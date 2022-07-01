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


# Retorna um usuário
# TODO: Parece não ter utilidade, se ao final do projeto ainda não tiver remover
@app.get("/users/{user_id}/", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


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
@app.post("/movie/{movie_name}/comment/{user_id}/")
async def comment(movie_name: str, user_id: int):
    pass


# Edita comentário em filme
@app.put("/movie/{movie_name}/comment/{user_id}/")
async def edit_comment(movie_name: str, user_id: int):
    pass


# Deleta comentário em filme
@app.delete("/movie/{movie_name}/comment/{user_id}/")
async def delete_comment(movie_name: str, user_id: int):
    pass


# Responde comentário de filme
@app.post("/movie/{movie_name}/comment/{user_id}/reply/{reply_comment_id}/")
async def answer_comment(movie_name: str, user_id: int, reply_comment_id: int):
    pass


# Cita comentário de filme
@app.post("/movie/{movie_name}/comment/{user_id}/mention/{mention_comment_id}/")
async def mention_comment(movie_name: str, user_id: int, mention_comment_id: int):
    pass


# Responde e menciona comentário de filme
@app.post("/movie/{movie_name}/comment/{user_id}/reply/{reply_comment_id}/mention/{mention_comment_id}/")
async def mention_comment(movie_name: str, user_id: int, mention_comment_id: int):
    pass


# Marca com gostei ou não gostei um comentário de filme
@app.post("/comment/{comment_id}/like/{like}/")
async def evaluate_comment(comment_id: int, like: bool):
    pass


# Insere uma nota em filme
@app.post("/movie/rate/{movie_name}/{user_id}/")
async def evaluate(movie_name: str, user_id: int):
    pass


# transforma usuário em moderador
@app.post("/upgrade-user/{user_id}/")
async def upgrade_user(user_id: int):
    pass


# Marca um comentário como repetido
@app.post("/comment/{comment_id}/repeated/{repeated}/")
async def set_repeated(comment_id: int, repeated: bool):
    pass
