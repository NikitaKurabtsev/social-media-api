import pytest
from fastapi import HTTPException, status
from jose import jwt

from app import schemas
from app.config import settings
from app.oauth2 import verify_access_token


def test_login(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
            }
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")

    assert response.status_code == 200
    assert login_response.token_type == "bearer"
    assert id == int(test_user["id"])


def test_unauthorized_current_user(client, test_user):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_incorrect_username_login(client, test_user):
    response = client.post(
        "/login",
        data={"username": "wrong@gmail.com", "password": "password"}
    )

    assert response.status_code == 403
    assert response.json().get("detail") == "Invalid credentials"


def test_incorrect_password_login(client, test_user):
    response = client.post(
        "/login",
        data={"username": "nikita@gmail.com", "password": "wrong_password"}
    )

    assert response.status_code == 403
    assert response.json().get("detail") == "Invalid credentials"


def test_create_acess_token():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    with pytest.raises(HTTPException):
        verify_access_token("1234567", credentials_exception)
