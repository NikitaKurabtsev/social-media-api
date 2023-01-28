from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.config import settings
from app.database import Base, get_db


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


# @pytest.fixture
# def create_post(client):
#     post = client.post(
#         "/posts/",
#         json={"title": "post", "content": "content"},
#         auth={"nikita@gmail.com", "password"}
#     )

#     return post