from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostInput(PostBase):
    pass


class PostOutput(PostBase):
    created_at: datetime
    
    class Config:
        orm_mode = True
