from .routers import auth,todos,admin,Users
from fastapi import FastAPI,Request,status
from .models import base
from  .Database import engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()

base.metadata.create_all(bind= engine)


app.mount("/static",StaticFiles(directory="TODOAPP/static"),name="static")

@app.get("/")
def test(request:Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {"status":"healthy".casefold()}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(Users.router)











