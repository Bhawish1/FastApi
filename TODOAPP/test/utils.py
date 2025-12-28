from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import base,Todos,Users
from ..main import app
from fastapi.testclient import TestClient
import pytest

from ..routers.auth import bcrypt_context

SQl_Alchemy_Database_URl = "sqlite:///./test.db"
engine = create_engine(SQl_Alchemy_Database_URl
                       ,connect_args={"check_same_thread":False},
                       poolclass= StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try :
        yield db
    finally :
        db.close()

def override_get_current_user():
    return{"username":"Bhawish1","id":1,"role":"admin"}

Client = TestClient(app)

@pytest.fixture

def test_todo():
    todo = Todos(title ="Learn to code",
                 description="Because it's useful",
                 priority = 5,
                 complete =False,
                 owner_id=1)

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection :
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
@pytest.fixture
def test_user():
    user = Users(username ="Bhawish1",
                 email = "Bhawish040@gmail.com",
                 first_name = "Bhawish",
                 last_name = "Kumar",
                 hashed_password = bcrypt_context.hash("Bhawish12#"),
                 role = "admin",
                 Phone_number = "07884066699")

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection :
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

