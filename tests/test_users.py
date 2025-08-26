from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Peace, hello world!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/api/v1/users/", json={"email": "sam2@mydomain.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "sam2@mydomain.com"
    assert res.status_code == 201
