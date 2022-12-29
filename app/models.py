from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=True, server_default=text("now()"))
    owner = Column(String, ForeignKey("users.email", ondelete="CASCADE"),
                      nullable=False)
    owner_data = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=True, server_default=text("now()"))


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
        )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
        )
