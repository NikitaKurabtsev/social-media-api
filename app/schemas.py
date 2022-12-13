from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostInput(PostBase):
    pass


class PostOutput(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: str
    email: EmailStr

    class Config:
        orm_mode = True
