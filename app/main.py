from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    connection = psycopg2.connect(
        host='localhost', 
        database='social_media_api', 
        user='postgres', 
        password='prestigio', 
        cursor_factory=RealDictCursor
    )
    cursor = connection.cursor()
    print("Succesfull Database connection")
except Exception as error:
    print("Connecting to Databse failed")
    print(f"Error: {error}")


my_posts = [
    {"title": "test1", "content": "test_content1", "id": 1},
    {"title": "test2", "content": "test_content2", "id": 2}
]


def find_post(id):
    """Return post by id"""
    for obj in my_posts:
        if obj["id"] == id:
            return obj


def find_post_index(id):
    for i, obj in enumerate(my_posts):
        if obj["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "welcome to my API"}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id: {id} not found")
    return {"post": post}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post.dict()
    new_post["id"] = randrange(1, 500)
    my_posts.append(new_post)
    return {"message": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post_index(id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exists")
    my_posts.pop(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exists")
    updated_post = post.dict()
    updated_post["id"] = id
    my_posts[index] = updated_post
    return {"data": updated_post}
