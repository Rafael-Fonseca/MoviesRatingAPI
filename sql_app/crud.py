from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"  # TODO: HASHEIA!!!
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id)


def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_rating(db: Session, rating_id: int):
    return db.query(models.Rating).filter(models.Rating.id == rating_id)


def get_ratings_by_movie(db: Session, movie: str):
    return db.query(models.Rating).filter(models.Rating.movie == movie)


def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id)


def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Profile(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id)


def get_comments_by_movie(db: Session, movie: str):
    return db.query(models.Comment).filter(models.Comment.movie == movie)


def get_comments_by_user(db: Session, user_id: int):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id)


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Profile(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
