from fastapi import FastAPI
from fastapi.responses import Response
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index_page():
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    return Response(login_page, media_type="text/html")


@app.post("/login")
def get_success_login():
    return Response("All right!!!")
