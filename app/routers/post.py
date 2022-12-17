from typing import List

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOutput])
def get_posts(
    db: Session = Depends(get_db), 
    current_user = Depends(oauth2.get_current_user)
    ) -> List[models.Post]:
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return posts


@router.get("/{id}", response_model=schemas.PostOutput)
def get_post(id: int, db: Session = Depends(get_db)) -> models.Post:
    # cursor.execute(
    #     """
    #     SELECT *
    #     FROM posts
    #     WHERE id = %s
    #     """,
    #     (str(id))
    # )
    # post = cursor.fetchone()
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the id: {id} not found"
        )

    return post


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.PostOutput)
def create_post(post: schemas.PostInput,
                db: Session = Depends(get_db)) -> models.Post:
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, is_published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.is_published)
    # )
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)) -> None:
    # cursor.execute(
    #     """
    #     DELETE FROM posts
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (str(id))
    # )
    # post = cursor.fetchone()
    # connection.commit()
    post = db.query(models.Post).get(id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostOutput)
def update_post(id: int, updated_post: schemas.PostInput,
                db: Session = Depends(get_db)) -> models.Post:
    # cursor.execute(
    #     """
    #     UPDATE posts
    #     SET title=%s, content=%s, is_published=%s
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.is_published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # connection.commit()
    # post_query = db.query(models.Post).get(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()