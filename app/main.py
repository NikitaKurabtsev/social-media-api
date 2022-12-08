from random import randrange
from typing import Optional
import time
import os

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from dotenv import load_dotenv

from app.utils import FilePrinter, Logger, TerminalPrinter

load_dotenv()

logger = Logger()

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        connection = psycopg2.connect(
            host=os.getenv("HOST"), 
            database=os.getenv("DATABASE"), 
            user=os.getenv("PSQL_USER"), 
            password=os.getenv("PASSWORD"), 
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        logger.log("Succesfull Database connection", FilePrinter)
        break

    except Exception as error:
        logger.log(f"Connecting to Databse failed with error: {error}", FilePrinter)
        logger.log(f"Connecting failed, error: {error}", TerminalPrinter)
        time.sleep(5)


def find_post(id):
    """Return post by id"""
    for obj in my_posts:
        try:
            if obj["id"] == id:
                return obj
        except Exception as error:
            raise f"obj with id {id} does not exist"


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
