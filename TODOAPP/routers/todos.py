
from fastapi import FastAPI,Depends,HTTPException,Path,APIRouter,Request
from typing import Annotated
from sqlalchemy.orm import Session

from ..models import Todos,TodosRequest
from  ..Database import SessionLocal
from starlette import status
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="TODOAPP/template")

router = APIRouter(
    prefix= "/todos",
    tags=["todos"]
)



def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


db_Dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

####pages
@router.get("/todo-page")
async def render_todo_page(request:Request,db:db_Dependency):
    try :
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None :
            return redirect_to_login()
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todo.html",{"request":request,"todos":todos,"user":user})
    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_todo_page(request:Request):
    try:
        user= await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request":request,"user":user})
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_Dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id==todo_id).first()
        return templates.TemplateResponse("edit-todo.html",{"request":request,"todo":todo,"user":user})
    except:
        return redirect_to_login()





### Endpoints
@router.get("/")
async def read_all(user:user_dependency,db:db_Dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication Failed")
    return db.query(Todos).filter(Todos.owner_id==user.get("id")).all()

@router.get("/read_Todos/{Todos_id}",status_code = status.HTTP_200_OK)
async def read_todos_by_id(user:user_dependency,db:db_Dependency,Todos_id : int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication Failed")

    Todos_models = db.query(Todos).filter(Todos.id == Todos_id)\
        .filter(Todos.owner_id==user.get("id")).first()
    if Todos_models is not None :
        return Todos_models
    else :
        raise HTTPException(status_code=404, detail="Item not found for the specific id")

@router.get("/Todos/{todos_priority}",status_code = status.HTTP_200_OK)
async def read_todos_by_priority(user:user_dependency,db:db_Dependency,todos_priority:int= Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication Failed")

    Todos_models = db.query(Todos).filter(Todos.priority == todos_priority)\
        .filter(Todos.owner_id==user.get("id")).all()
    if not Todos_models :
        raise HTTPException(status_code=404, detail="Item not found for the specific priority")
    return Todos_models


@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todos(user:user_dependency,db:db_Dependency,todosrequest:TodosRequest):
    if user is None :
        raise HTTPException(status_code=401,detail="authentication Failed")
    todo_model = Todos(**todosrequest.model_dump(),owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
@router.put("/update_todos/{todos_id}",status_code= status.HTTP_204_NO_CONTENT)
async def update_todos(user:user_dependency,db:db_Dependency,todosrequest:TodosRequest,todos_id:int = Path(gt=0)):
    if user is None :
        raise HTTPException(status_code=401,detail="authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todos_id).first()
    if todo_model is None :
        raise HTTPException(status_code=404, detail="Item not found for the specific id")
    else :
        todo_model.title = todosrequest.title
        todo_model.description = todosrequest.description
        todo_model.priority = todosrequest.priority
        todo_model.complete = todosrequest.complete
        db.add(todo_model)
        db.commit()

@router.delete("/delete_todos/{todos_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user:user_dependency,db:db_Dependency,todos_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id==todos_id).first()
    if todo_model is not None :
        db.query(Todos).filter(Todos.id == todos_id).delete()
        db.commit()

    else :
        raise HTTPException(status_code=404, detail="Item not found for the specific id or has already been deleted")
@router.delete("/delete_todos_by_priority/{todos_priority}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos_by_priority(user:user_dependency,db:db_Dependency,todos_priority:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.priority==todos_priority)\
        .filter(Todos.owner_id==user.get("id")).all()
    if not todo_model :
        raise HTTPException(status_code=404, detail="Item not found for the specific id or has already been deleted")
    else :
        db.query(Todos).filter(Todos.priority==todos_priority)\
            .filter(Todos.owner_id==user.get("id")).delete()
        db.commit()
    return todo_model