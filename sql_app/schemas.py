from pydantic import BaseModel
from datetime import datetime


class RatingBase(BaseModel):
    movie: str
    evaluation: int


class RatingCreate(RatingBase):
    user_id: int


class Rating(RatingBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    description: str
    movie: str
    respond_to: int
    mention_to: int
    create_at: datetime
    user_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    like: int
    dislike: int
    repeated: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    score: int
    profile_id: int
    evaluations: list[Rating] = []
    comments: list[Comment] = []

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    name: str
    min_score: int
    can_comment: bool
    can_evaluate_movies: bool
    can_read: bool
    can_answer_comments: bool
    can_mention_comments: bool
    can_evaluate_comments: bool
    can_delete_comments: bool
    can_mark_comment_as_repeated: bool
    can_turn_user_into_moderator: bool


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True
