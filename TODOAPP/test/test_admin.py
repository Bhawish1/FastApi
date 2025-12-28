from .utils import *
from ..routers.admin import get_db,get_current_user
from starlette import status


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

def test_read_all_authenticated(test_todo):
    response = Client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": "Learn to code",
                                "description": "Because it's useful",
                                 "priority": 5,
                                 "complete": False,
                                 "owner_id": 1,
                                "id": 1}]

def test_delete_by_1_authenticated(test_todo):
    response = Client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).all()
    assert model == []
