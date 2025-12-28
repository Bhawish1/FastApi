from ..routers.todos import get_db,get_current_user
from fastapi import status
from .utils import *


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

def test_read_all_authenticated(test_todo):
    response = Client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()== [{"complete":False,
                               "title":"Learn to code",
                               "description":"Because it's useful",
                               "id":1,
                               "owner_id":1,
                               "priority":5}]
def test_read_all_authenticate(test_todo):
    response = Client.get("todos/read_Todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()== {"complete":False,
                               "title":"Learn to code",
                               "description":"Because it's useful",
                               "id":1,
                               "owner_id":1,
                               "priority":5}


def test_todo_not_found(test_todo):
    response = Client.get("todos/read_Todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()== {"detail": "Item not found for the specific id"}


def test_create_todo(test_todo):
    request_data = {"title":"New Todo",
                    "description":"more information",
                    "owner_id":1,
                    "priority":2,
                    "complete":False}
    response = Client.post("todos/create_Todos",json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id==2).first()
    assert todo_model.title == request_data.get("title")

def test_update_todo(test_todo):
    request_data = {"title":"something something",
                    "description":"better than nothing",
                    "owner_id":1,
                    "priority":2,
                    "complete":True}
    response = Client.put("todos/update_todos/1",json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get("title")

def test_delete_todo(test_todo):
    response = Client.delete("todos/delete_todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_by_priority(test_todo):
    response = Client.delete("todos/delete_todos_by_priority/5")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.priority == 5).all()
    assert model == []

