import tests.conftest
import pytest
import app.schemas as schemas

#TODO: implement code and test so user can't vote on own post
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0][0], "dir": 1})
    assert res.status_code == 204

def test_vote_twice_post(authorized_client, test_posts):
    post_id = test_posts[0][0]
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    res2 = authorized_client.get(f"/posts/{post_id}")
    res3 = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    res4 = authorized_client.get(f"/posts/{post_id}")
    post1 = schemas.Post(**res2.json())
    post2 = schemas.Post(**res4.json())
    assert post1.number_votes == post2.number_votes

def test_remove_vote(authorized_client, test_posts):
    post_id = test_posts[0][0]
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    res2 = authorized_client.get(f"/posts/{post_id}")
    res3 = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    res4 = authorized_client.get(f"/posts/{post_id}")
    post1 = schemas.Post(**res2.json())
    post2 = schemas.Post(**res4.json())
    assert post1.number_votes - 1 == post2.number_votes

def test_remove_vote_twice(authorized_client, test_posts):
    post_id = test_posts[0][0]
    res = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    res2 = authorized_client.get(f"/posts/{post_id}")
    res3 = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    res4 = authorized_client.get(f"/posts/{post_id}")
    post1 = schemas.Post(**res2.json())
    post2 = schemas.Post(**res4.json())
    assert post1.number_votes == post2.number_votes

def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 999999999999, "dir": 0})
    assert res.status_code == 404

def test_unauthorized_user_update_posts(unauthorized_client, testing_other_user_post):
    post_id = testing_other_user_post[0]
    res = unauthorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert res.status_code == 401