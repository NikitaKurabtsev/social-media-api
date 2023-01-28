from app import schemas
from app.config import settings
from jose import jwt


def test_login(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]}
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
