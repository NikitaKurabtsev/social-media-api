from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostInput(PostBase):
    pass


class PostOutput(PostBase):
    title: str
    content: str
    is_published: bool
