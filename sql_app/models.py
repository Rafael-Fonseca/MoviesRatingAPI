from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    score = Column(Integer)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="users")
    evaluations = relationship("Rating", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    min_score = Column(Integer)
    can_comment = Column(Boolean)
    can_evaluate_movies = Column(Boolean)
    can_read = Column(Boolean)
    can_answer_comments = Column(Boolean)
    can_mention_comments = Column(Boolean)
    can_evaluate_comments = Column(Boolean)
    can_delete_comments = Column(Boolean)
    can_mark_comment_as_repeated = Column(Boolean)
    can_turn_user_into_moderator = Column(Boolean)

    users = relationship("User", back_populates="profile")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie = Column(String)
    evaluation = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="evaluations")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    movie = Column(String)
    respond_to = Column(Integer)
    mention_to = Column(Integer)
    like = Column(Integer)
    dislike = Column(Integer)
    repeated = Column(Boolean)
    create_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")
