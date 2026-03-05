import tests.conftest
import pytest
import app.schemas as schemas

def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts")
    results = res.json()
    assert res.status_code == 200
    titles = ['first title', '2nd title', '3rd title']
    for i in range(len(results)):
        assert results[i]['title'] in titles

def test_unauthorized_user_get_all_posts(unauthorized_client):
    res = unauthorized_client.get("/posts")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(unauthorized_client, test_max_post_id):
    id = test_max_post_id[0]
    res = unauthorized_client.get(f"/posts/{id}")
    assert res.status_code == 401

def test_get_post_not_exist(authorized_client):
    res = authorized_client.get("/posts/9999999999")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published",[
    ("awesome new title", "awesome new context", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts", json={"title": title, "content": content, 
                                                 "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user.id == test_user.get('id')

def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts", json={"title": "a title", "content": "yada yada"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "a title"
    assert created_post.content == "yada yada"
    assert created_post.published == True
    assert created_post.user.id == test_user.get('id')

def test_unauthorized_user_create_post(unauthorized_client):
    res = unauthorized_client.post(
        "/posts", json={"title": "arbitrary title", "content": "aasdfdijasdf"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(unauthorized_client, test_max_post_id):
    id = test_max_post_id[0]
    res = unauthorized_client.delete(f"/posts/{id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_max_post_id):
    id = test_max_post_id[0]
    res = authorized_client.delete(f"/posts/{id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete("/posts/80000000000")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, testing_other_user_post):
    post_id = testing_other_user_post[0]
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    post_id = test_posts[0][0]
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": post_id
    }
    res = authorized_client.put(f"/posts/{post_id}", json=data)
    assert res.status_code == 200
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client, testing_other_user_post):
    post_id = testing_other_user_post[0]
    data = {
        "title": "more updated title",
        "content": "more updated content",
        "id": post_id
    }
    res = authorized_client.put(f"/posts/{post_id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_posts(unauthorized_client, testing_other_user_post):
    post_id = testing_other_user_post[0]
    res = unauthorized_client.put(f"/posts/{post_id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts):
    post_id = test_posts[0][0]
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": post_id
    }
    res = authorized_client.put("/posts/80000000000", json=data)
    assert res.status_code == 404