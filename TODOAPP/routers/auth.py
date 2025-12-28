from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException,Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..Database import SessionLocal
from ..models import UsersRequest,Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import timedelta,datetime,timezone
from jose import jwt,JWTError
from starlette import status
from fastapi.templating import Jinja2Templates
import os

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
OAUTH2_Bearer= OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter(
    prefix="/auth",
    tags= ["auth"])

Secret_Key = os.getenv("SECRET_KEY")
Algorithm = "HS256"

class Token(BaseModel):
    access_token : str
    token_type : str



def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


db_Dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="TODOAPP/template")

### pages
@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.get("/register-page")
def render_register_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})

###
### Endpoints
def create_token(username:str,user_id:int,role:str,expires_delta:timedelta):
    encode = {"sub":username,
              "user_id":user_id,
              "role":role}
    expires=  datetime.now(timezone.utc)+ expires_delta
    encode.update({"exp":int(expires.timestamp())})
    return jwt.encode(encode,Secret_Key,algorithm=Algorithm)

async def get_current_user(token: Annotated[str,Depends(OAUTH2_Bearer)]):
    try:
        payload = jwt.decode(token,Secret_Key,algorithms=[Algorithm])
        username : str= payload.get("sub")
        user_id :int = payload.get("user_id")
        role : str = payload.get("role")
        if username is None  or user_id is None:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail= "could not validate user.")
        return {"username":username,"id":user_id,"role":role}
    except JWTError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user.")


def authenticate_user(username:str,password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None :
        return False
    if not bcrypt_context.verify(password,user.hashed_password) :
        return False
    return user

@router.post("/")
async def create_user(db : db_Dependency,userRequest:UsersRequest):
    create_User = Users(email = userRequest.email,
                        username = userRequest.username,
                        first_name = userRequest.first_name,
                        last_name = userRequest.last_name,
                        role = userRequest.role,
                        hashed_password = bcrypt_context.hash(userRequest.password),
                        is_active = True,
                        phone_number = userRequest.phone_number)
    db.add(create_User)
    db.commit()




@router.post("/token/",response_model=Token)
async def login_for_authentication(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
                                   db:db_Dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user.")
    token = create_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {"access_token":token, "token_type": "bearer"}





