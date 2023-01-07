from typing import List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostLikeOutput])
def get_posts(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
    search: Optional[str] = "",
    limit = 5, 
    skip = 0,
    ) -> List[models.Post]:
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # return only current users posts
    # posts = db \
    #     .query(models.Post) \
    #     .filter(models.Post.owner == current_user.username) \
    #     .all()
  
    posts = db \
        .query(models.Post, func.count(models.Like.post_id).label("likes")) \
        .join(
            models.Like, 
            models.Post.id == models.Like.post_id, 
            isouter=True
            ) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(skip) \
        .all()

    return posts

 
@router.get("/{id}", response_model=schemas.PostLikeOutput)
def get_post(
    id: int, db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user)
    ) -> models.Post:
    # cursor.execute(
    #     """
    #     SELECT *
    #     FROM posts
    #     WHERE id = %s
    #     """,
    #     (str(id))
    # )
    # post = cursor.fetchone()
    post = db \
        .query(models.Post, func.count(models.Like.post_id).label("likes")) \
        .join(
            models.Like, 
            models.Post.id == models.Like.post_id, 
            isouter=True
            ) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id) \
        .first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with the id: {id} not found"
        )

    return post


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.PostOutput)
def create_post(
    post: schemas.PostInput,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user)
    ) -> models.Post:
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
    print(current_user)
    new_post = models.Post(**post.dict())
    new_post.owner = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user)
    ) -> None:
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
    if post.owner != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"you not the owner of this post"
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostOutput)
def update_post(
    id: int, updated_post: schemas.PostInput,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user)
    ) -> models.Post:
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
    if post.owner != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"you not the owner of this post"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
