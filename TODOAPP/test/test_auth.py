from .utils import *
from ..routers.auth import get_db,authenticate_user,create_token,Secret_Key, Algorithm,get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username,"Bhawish12#",db)
    assert authenticated_user is not None
    assert  authenticated_user.username == test_user.username

    Non_existent_user = authenticate_user("Wrongname","Bhawish12#",db)
    assert Non_existent_user is False
    Wrong_password = authenticate_user(test_user.username,"Wrongname",db)
    assert  Wrong_password is False


def test_create_access_token():

    token = create_token("Bhawish1","example@gmail.com",1,
                         "user", timedelta(days=1))
    decoded_token = jwt.decode(token,Secret_Key,algorithms=[Algorithm],options={"verify_signature":False})
    assert decoded_token["user_id"] == 1
    assert decoded_token["email"] == "example@gmail.com"
@pytest.mark.asyncio
async def test_current_user():
    encode = {"sub":"Bhawish1","user_id":1,"email":"@gmail.com","role":"admin"}
    token = jwt.encode(encode,Secret_Key,algorithm=Algorithm)
    user = await get_current_user(token=token)
    assert user == {"username":"Bhawish1",
                    "email":"@gmail.com",
                    "id":1,
                    "role":"admin"}

@pytest.mark.asyncio
async def test_current_user_missing_payload():
    encode = {"sub":"admin"}
    token = jwt.encode(encode,Secret_Key,algorithm=Algorithm)
    with pytest.raises(HTTPException) as exicinfo:
         await get_current_user(token=token)

    assert exicinfo.value.status_code == 401
    assert exicinfo.value.detail == "could not validate user."








