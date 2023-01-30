def test_create_vote(authorized_client, test_posts):
    data = {"post_id": test_posts[0].id, "direction": 1}
    response = authorized_client.post("/likes/", json=data)

    assert response.status_code == 201
    assert response.json() == f"you like a post with id: 1" 


def test_like_post_that_not_exists(authorized_client):
    data = {"post_id": 5, "direction": 1}
    response = authorized_client.post("/likes/", json=data)

    assert response.json().get("detail") == "post with id 5 not found"


def test_like_already_liked_post(authorized_client, test_posts, test_user):
    user = test_user["id"]
    data = {"post_id": test_posts[0].id, "direction": 1}
    authorized_client.post("/likes/", json=data)
    response = authorized_client.post("/likes/", json=data)

    assert response.json().get("detail") == (
        f"user with id: {user} " 
        f"already likes post with id: 1"
        )


def test_delete_like(authorized_client, test_posts):
    data = {"post_id": test_posts[0].id, "direction": 1}
    delete_data = {"post_id": test_posts[0].id, "direction": 0}
    authorized_client.post("/likes/", json=data)
    response = authorized_client.post("/likes/", json=delete_data)

    assert response.json() == {"message": "like delete successful"}


def test_delete_like_that_not_exists(authorized_client, test_posts):
    data = {"post_id": test_posts[1].id, "direction": 0}
    response = authorized_client.post("/likes/", json=data)

    assert response.status_code == 404
    assert response.json().get("detail") == "like does not exists"
