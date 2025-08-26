from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Peace, hello world!"
    assert res.status_code == 200