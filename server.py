from fastapi import FastAPI, Form
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
def get_success_login(email: str = Form(...), password: str = Form(...)):
    return Response(f"Your username: {email}, password: {password}", media_type="text/html")

