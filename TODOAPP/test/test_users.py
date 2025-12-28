from .utils import *
from ..routers.Users import get_db,get_current_user
from starlette import status


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

def test_read_user_authenticated(test_user):
    response = Client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "Bhawish1"
def test_change_password_user_authenticated(test_user):
    response = Client.put("/users/password",json={"password":"Bhawish12#","new_password":"Bhawish#" })

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_user_invalid_current_password(test_user):
    response = Client.put("/users/password", json={"password": "Bhawish12",
                                                   "new_password": "Bhawish#"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
