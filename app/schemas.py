from datetime import datetime
from typing import Optional
from pydantic.types import conint

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostInput(PostBase):
    pass


class PostOutput(PostBase):
    id: int
    created_at: datetime
    owner_data: UserOutput

    class Config:
        orm_mode = True


class PostLikeOutput(BaseModel):
    Post: PostOutput
    likes: int


class LikeInput(BaseModel):
    post_id: int
    direction: conint(le=1, ge=0)
