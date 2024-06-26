import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [("awesome new title", "awesome new content", True),
                                                       ("favorite pizza", "i love pepperoni", False),
                                                       ("tallest skyscrapers", "wahoo", True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published":published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "some title", "content": "some content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "some title"
    assert created_post.content == "some content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "some title", "content": "some content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    print(test_posts[0].id)
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json={"title": "Updated title", "content": "Updated content", "published": False})
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == "Updated title"
    assert updated_post.content == "Updated content"


def test_update_post_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[5].id}", json={"title": "Updated title", "content": "Updated content"})
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == "Updated title"
    assert updated_post.content == "Updated content"
    assert updated_post.published == True


def test_update_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json={"title": "Updated title", "content": "Updated content"})
    assert res.status_code == 403


def test_update_post_by_unauthorized_user(client, test_posts):
    res = client.put(f"/posts/{test_posts[3].id}", json={"title": "Updated title", "content": "Updated content"})
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.put(f"/posts/999", json={"title": "Updated title", "content": "Updated content"})
    assert res.status_code == 404
