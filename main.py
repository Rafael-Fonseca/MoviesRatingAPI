from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
import httpx

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


client = httpx.AsyncClient()


# TODO: Colocar mensagem informando url correta, local de documentação...  postgress EDB pgadmin
@app.get("/")
async def root():
    return {"message": "Olá! tente adicionar /docs ao final da url para ver a documentação desta api no padrão swagger"}


# Registra o usuário
@app.post("/signup/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Este username já está cadastrado")
    return crud.create_user(db=db, user=user)


'''
# TODO: Remover, pois Este endpoint não deve existir, mas vou deixar ele aqui de exemplo para mim mesmo
@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
'''


# Loga um usuário
@app.post("/signin/")
async def authenticate():
    pass


# Devolve todas as informações de um filme
# TODO: Capturar informações do filme que estão no banco de dados
# TODO: Criar modelo movie Pydantico para retornar apenas as informações desejadas
@app.get("/movie/{movie_name}/", response_model=schemas.Movie)
async def read_movie(movie_name: str):
    base_url = 'http://www.omdbapi.com/?apikey=4f23974&t='
    complement = movie_name.strip().replace(' ', '+')
    response = await client.get(base_url + complement)
    return schemas.MovieCreate(**response.json())


# Insere comentário em filme
@app.post("/movie/comment/")
async def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)


# Edita comentário em filme
# TODO: Garantir que esteja alterando um comentário dele.
@app.put("/movie/comment/{comment_id}")
async def edit_comment(comment: schemas.CommentCreate, comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    comment_edited = crud.edit_comment(db=db, comment=comment, comment_id=comment_id)
    if not comment_edited:
        raise HTTPException(status_code=400, detail="Você não pode alterar o filme ou o dono de um comentário.")

    return crud.edit_comment(db=db, comment=comment, comment_id=comment_id)


# Deleta comentário em filme
@app.delete("/movie/comment/{comment_id}/")
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    # TODO: Garantir que seja um comentário dele
    return crud.delete_comment(db=db, db_comment=db_comment)


# Responde comentário de filme
# TODO: PODE GERAR ERROS MECHER EM BD TRY CATCH
@app.post("/movie/comment/reply/")
async def answer_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment_to_reply = crud.get_comment(db, comment_id=comment.respond_to)
    if not db_comment_to_reply:
        raise HTTPException(status_code=404, detail="Comentário a ser respondido não encontrado")

    if db_comment_to_reply.movie != comment.movie:
        raise HTTPException(status_code=400, detail="Você não pode responder um comentário de filme diferente")

    if comment.mention_to == 0:
        comment.mention_to = None

    return crud.create_comment(db=db, comment=comment)


# Cita comentário de filme
# TODO: Validações de filme devem considerar tudo em minusculo.
@app.post("/movie/comment/mention/")
async def mention_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment_to_mention = crud.get_comment(db, comment_id=comment.mention_to)
    if not db_comment_to_mention:
        raise HTTPException(status_code=404, detail="Comentário a ser mencionado não encontrado")

    if db_comment_to_mention.movie != comment.movie:
        raise HTTPException(status_code=400, detail="Você não pode citar um comentário de filme diferente")

    if comment.respond_to == 0:
        comment.respond_to = None

    return crud.create_comment(db=db, comment=comment)


# Responde e menciona comentário de filme
@app.post("/movie/comment/maximum/")
async def create_max_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment_to_reply = crud.get_comment(db, comment_id=comment.respond_to)
    db_comment_to_mention = crud.get_comment(db, comment_id=comment.mention_to)
    if not db_comment_to_reply or not db_comment_to_mention:
        raise HTTPException(status_code=404, detail="Comentário a ser respondido ou mencionado não encontrado")

    if (db_comment_to_reply.movie.lower() != comment.movie.lower()
            or db_comment_to_mention.movie.lower() != comment.movie.lower()):
        raise HTTPException(status_code=400, detail="Você só pode citar e responder comentários do mesmo filme")

    return crud.create_comment(db=db, comment=comment)


# Marca com gostei ou não gostei um comentário de filme
@app.post("/movie/comment/{comment_id}/like/{like}/")
async def evaluate_comment(comment_id: int, like: bool, db: Session = Depends(get_db)):
    #TODO: Confere se usuário atual tem poder para isso
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    if db_comment.like is None:
        db_comment.like = 0

    if db_comment.dislike is None:
        db_comment.dislike = 0

    return crud.evaluate_comment(db, db_comment, like)


# Insere uma nota em filme
@app.post("/movie/rate/")
async def evaluate(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    db_rating = crud.get_ratings_by_movie_and_user(db, rating.user_id, rating.movie)
    if db_rating:
        # TODO: conferir se dono desta avaliação é o usuário atual
        return crud.edit_rating(db, rating, db_rating)
    else:
        crud.create_rating(db, rating=rating)
        return crud.add_user_score(db, crud.get_user(db, rating.user_id))


# transforma usuário em moderador
@app.post("/upgrade-user/{user_id}/")
async def upgrade_user(user_id: int, db: Session = Depends(get_db)):
    #TODO: Conferir se usuário atual é moderador
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return crud.upgrade_user_by_moderator(db, db_user)


# Marca um comentário como repetido
@app.post("/comment/{comment_id}/repeated/{repeated}/")
async def set_repeated(comment_id: int, repeated: bool, db: Session = Depends(get_db)):
    #TODO: Conferir se usuário atual é moderador
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    return crud.comment_repeated(db, db_comment, repeated)
