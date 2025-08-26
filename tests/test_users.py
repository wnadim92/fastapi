from app import schemas
from .database import client, session
import pytest

@pytest.fixture
def test_user(client):
    user_data = {"email": "sam1@mydomain.com", "password": "password123"}
    res = client.post("/api/v1/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

def test_create_user(client):
    res = client.post("/api/v1/users/", json={"email": "sam2@mydomain.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "sam2@mydomain.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/api/v1/login/", data={"username": test_user['email'], "password": test_user['password']})
    print(res.json())
    assert res.status_code == 200

