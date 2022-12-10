from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class InputPost(PostBase):
    pass
