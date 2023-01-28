from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app import models


engine = create_engine(
    f"postgresql"
    f"://{settings.database_username}"
    f":{settings.database_password}"
    f"@{settings.database_hostname}"
    f":{settings.database_port}"
    f"/test_{settings.database_name}"
    )

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    data = {"email": "nikita@gmail.com", "password": "password"}
    response = client.post("/users/", json=data)
    user = response.json()
    user['password'] = data['password']

    return user


@pytest.fixture
def test_user_2(client):
    data = {"email": "test@gmail.com", "password": "password"}
    response = client.post("/users/", json=data)
    user = response.json()
    user['password'] = data['password']

    return user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_user_not_post_owner(client):
    data = {"email": "test@gmail.com", "password": "password"}
    response = client.post("/users/", json=data)
    user = response.json()
    user['password'] = data['password']

    return user


@pytest.fixture
def test_posts(test_user, test_user_2, session):
    posts_data = [
        {
            "title": "test_post_1",
            "content": "test_content_1",
            "owner": test_user["id"] 
        },
        {
            "title": "test_post_2",
            "content": "test_content_2",
            "owner": test_user["id"] 
        },
        {
            "title": "test_post_2",
            "content": "test_content_2",
            "owner": test_user_2["id"]
        }
    ]
    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()
