from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, post, user, like

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/")
def root():
    return {"message": "welcome to my API"}
