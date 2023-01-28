def test_get_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    response.status_code == 200


def test_get_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 200


def test_get_posts_does_not_exists(authorized_client):
    response = authorized_client.get("/posts/1")

    assert response.status_code == 404
    assert response.json().get("detail") == f"post with the id: 1 not found"


def test_create_post(authorized_client):
    data = {"title": "test_post", "content": "test_content"}
    response = authorized_client.post("/posts/", json=data)

    assert response.status_code == 201


def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204


def test_delete_post_that_not_exists(authorized_client):
    response = authorized_client.delete("/posts/1")

    assert response.status_code == 404
    assert response.json().get("detail") == "post with id: 1 does not exists"


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[2].id}")

    assert response.status_code == 405
    assert response.json().get("detail") == "you not the owner of this post"


def test_update_post(authorized_client, test_posts):
    data = {"title": "test_post", "content": "updated_content"}
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    assert response.status_code == 200


def test_update_post_that_not_exists(authorized_client):
    data = {"title": "test_post", "content": "updated_content"}
    response = authorized_client.put("/posts/1", json=data)

    assert response.status_code == 404
    assert response.json().get("detail") == "post with id: 1 does not exists"


def test_update_other_post(authorized_client, test_posts):
    data = {"title": "test_post", "content": "updated_content"}
    response = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)

    assert response.status_code == 405
    assert response.json().get("detail") == "you not the owner of this post"
