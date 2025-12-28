from .Database import base
from pydantic import BaseModel,Field
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(base) :
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index= True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default= True)
    role = Column(String)
    phone_number = Column(String)

class UsersRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str
    phone_number : str = Field(min_length=11)
class Todos(base) :
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index= True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

class TodosRequest(BaseModel):
    title : str= Field(min_length= 5, max_length = 20)
    description : str = Field(min_length=10, max_length = 100)
    priority : int = Field(ge= 1, le= 10)
    complete : bool