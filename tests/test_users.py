from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from dotenv import load_dotenv
import os
from app.config import settings
 

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Peace, hello world!"
    assert res.status_code == 200

def test_create_user():
    res = client.post("/api/v1/users/", json={"email": "sanjeev2@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "sanjeev2@gmail.com"
    assert res.status_code == 201
