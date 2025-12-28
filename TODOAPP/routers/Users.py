
from fastapi import FastAPI,Depends,HTTPException,Path,APIRouter
from typing import Annotated
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from ..models import Users, UsersRequest
from passlib.context import CryptContext
from ..models import Todos,TodosRequest
from  ..Database import SessionLocal
from starlette import status
from .auth import get_current_user,bcrypt_context


router = APIRouter(
    prefix="/users",
    tags= ["users"]
)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

db_Dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
class UserVerification(BaseModel):
    password : str
    new_password : str = Field(min_length=6,max_length=15)

@router.get("/",status_code=status.HTTP_200_OK)
async def read_user(user:user_dependency,db:db_Dependency):
    if user is None :
        raise HTTPException(status_code=401,detail="Authentication Failed")
    return db.query(Users).filter(Users.id==user.get("id")).first()

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_Dependency,user_verification:UserVerification):
    if user is None :
        raise HTTPException(status_code=401,detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id==user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail="Old password doesn't match")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/Phone_number",status_code=status.HTTP_204_NO_CONTENT)
async def add_phone_number(user:user_dependency,db:db_Dependency,phone_number:str):
    if user is None :
        raise HTTPException(status_code=401, detail="authentication Failed")
    user_model = db.query(Users).filter(Users.id ==user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()





