from sqlalchemy import Column, Integer, DateTime, Text, Boolean, Float, VARCHAR, ForeignKey
from sqlalchemy.orm import as_declarative
from typing import Any, ClassVar
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        unique=True,
    )
    first_name = Column(VARCHAR(256), nullable=False)
    last_name = Column(VARCHAR(256), nullable=False)
    password = Column(Text, nullable=False)
    login = Column(VARCHAR(256), unique=True, nullable=False)


class PostModel(Base):
    __tablename__ = "posts"
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        unique=True,
    )
    user_id = Column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    text = Column(Text, nullable=False)

