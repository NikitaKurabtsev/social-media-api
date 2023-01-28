from app import schemas


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

    assert response.status_code == 200


def test_get_not_exists_user(client):
    response = client.get("/users/2")

    assert response.status_code == 404
    assert response.json().get("detail") == "user with id: 2 does not exist"
