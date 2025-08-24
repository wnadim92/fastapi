from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
import os

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res)