from sqlalchemy.orm import Session

from . import models, schemas
from passlib.context import CryptContext


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate, profile_id: int = 0, score: int = 0):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password,
                          profile_id=profile_id, score=score)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_user_score(db: Session, db_user: models.User):
    db_user.score += 1
    db.commit()
    db.refresh(db_user)
    if db_user.profile.id < 3:
        return upgrade_user(db, db_user, get_profile(db, db_user.profile_id + 1))


def upgrade_user(db: Session, db_user: models.User, db_profile: models.Profile):
    if db_user.score >= db_profile.min_score:
        db_user.profile_id += 1
        db.commit()
        db.refresh(db_user)
        return "Operação realizada e o usuário subiu o nível do seu perfil!"


def upgrade_user_by_moderator(db: Session, db_user: models.User):
    db_user.profile_id = 3
    db.commit()
    db.refresh(db_user)
    return db_user


def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_rating(db: Session, rating_id: int):
    return db.query(models.Rating).filter(models.Rating.id == rating_id).first()


def get_ratings_by_movie(db: Session, movie: str):
    return db.query(models.Rating).filter(models.Rating.movie == movie).all()


def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id).all()


def get_ratings_by_movie_and_user(db: Session, user_id: int, movie: str):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id, models.Rating.movie == movie).first()


def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def edit_rating(db: Session, rating: schemas.RatingCreate, db_rating: models.Rating):
    db_rating.evaluation = rating.evaluation
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_comments_by_movie(db: Session, movie: str):
    return db.query(models.Comment).filter(models.Comment.movie == movie)


def get_comments_by_user(db: Session, user_id: int):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id)


def create_comment(db: Session, comment: schemas.CommentCreate):
    plain_comment = comment.dict()
    plain_comment['movie'] = plain_comment['movie'].lower()
    db_comment = models.Comment(**plain_comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def edit_comment(db: Session, comment: schemas.CommentCreate, comment_id: int):
    to_update_comment = db.query(models.Comment).filter_by(id=comment_id).first()
    if to_update_comment.movie != comment.movie or to_update_comment.user_id != comment.user_id:
        return False
    to_update_comment.description = comment.description

    db.commit()
    db.refresh(to_update_comment)
    return to_update_comment


def delete_comment(db: Session, db_comment: models.Comment):
    db.delete(db_comment)
    db.commit()
    return "Comentário deletado"


def evaluate_comment(db: Session, db_comment: models.Comment, evaluate: bool):
    if evaluate:
        db_comment.like += 1
    else:
        db_comment.dislike += 1

    db.commit()
    db.refresh(db_comment)
    return db_comment


def comment_repeated(db: Session, db_comment: models.Comment, repeated: bool):
    db_comment.repeated = repeated
    db.commit()
    db.refresh(db_comment)
    return db_comment
