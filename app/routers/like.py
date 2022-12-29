from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(
    like: schemas.LikeInput,
    db: Session = Depends(database.get_db),
    current_user: str = Depends(oauth2.get_current_user)
    ):
    post_query = db \
        .query(models.Post) \
        .filter(models.Post.id == like.post_id) \
        .first()

    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {like.post_id} not found"
        )
    like_query = db \
        .query(models.Like) \
        .filter(
            models.Like.post_id == like.post_id,
            models.Like.user_id == current_user.id
            )
    found_like = like_query.first()
    if like.direction == 1:
        if found_like:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"user with id: {current_user.id} "
                f"already likes post with id: {like.post_id}"
            )
        )
        # new_like = models.Like(**like.dict())
        new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()

        return f"you like a post with id: {like.post_id}"
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="like does not exists"
            )
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "like delete successful"}
