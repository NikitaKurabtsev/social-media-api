from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from fastapi.security.oauth2 import (
    OAuth2PasswordRequestForm, OAuth2PasswordBearer
)
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2
from ..utils import verify_password

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
    ) -> schemas.Token:
    user = db \
        .query(models.User) \
        .filter(models.User.email == user_credentials.username) \
        .first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials"
            )
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials"
            )
    access_token = oauth2.create_access_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
