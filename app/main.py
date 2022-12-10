import os
import time
from random import randrange
from typing import Optional

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils import FilePrinter, Logger, TerminalPrinter
from app import models
from app.database import engine, SessionLocal

load_dotenv()

logger = Logger()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


@app.get("/")
def root():
    return {"message": "welcome to my API"}


@app.get("/sqlalchemy")
def sqlalchemy_data(db: Session = Depends(get_db)):
    return {"data": "Success"}


# while True:
#     try:
#         connection = psycopg2.connect(
#             host=os.getenv("HOST"), 
#             database=os.getenv("DATABASE"), 
#             user=os.getenv("PSQL_USER"), 
#             password=os.getenv("PASSWORD"), 
#             cursor_factory=RealDictCursor
#         )
#         cursor = connection.cursor()
#         logger.log("Succesfull Database connection", FilePrinter)
#         break

#     except Exception as error:
#         logger.log(f"Connecting to Databse failed with error: {error}", FilePrinter)
#         logger.log(f"Connecting failed, error: {error}", TerminalPrinter)
#         time.sleep(5)


# @app.get("/")
# def root():
#     return {"message": "welcome to my API"}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}


# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute(
#         """
#         SELECT * 
#         FROM posts 
#         WHERE id = %s
#         """,
#         (str(id))
#     )
#     post = cursor.fetchone()

#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with the id: {id} not found"
#         )

#     return {"post": post}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute(
#         """
#         INSERT INTO posts (title, content, is_published) 
#         VALUES (%s, %s, %s) 
#         RETURNING *
#         """, 
#         (post.title, post.content, post.is_published)
#     )
#     new_post = cursor.fetchone()
#     connection.commit()

#     return {"message": new_post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(
#         """
#         DELETE FROM posts 
#         WHERE id = %s 
#         RETURNING *
#         """, 
#         (str(id))
#     )
#     post = cursor.fetchone()
#     connection.commit()
    
#     if post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail=f"post with id: {id} does not exists"
#         )
            
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute(
#         """
#         UPDATE posts
#         SET title=%s, content=%s, is_published=%s
#         WHERE id = %s
#         RETURNING *
#         """,
#         (post.title, post.content, post.is_published, str(id))
#     )
#     updated_post = cursor.fetchone()
#     connection.commit()

#     if update_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} does not exists"
#         )

#     return {"data": updated_post}
