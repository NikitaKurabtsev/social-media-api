from app import schemas
from tests.database import client, test_user, session


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "welcome to my API"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "nikita@gmail.com", "password": "password"}
    )
    new_user = schemas.UserOutput(**response.json())

    assert response.status_code == 201
    assert new_user.email == "nikita@gmail.com"


def test_get_user(client, test_user):
    response = client.get("/users/1")
    wrong_response = client.get("/users/2")

    assert response.status_code == 200
    assert wrong_response.status_code == 404
