from fastapi import FastAPI, Form
from fastapi.responses import Response
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# simplified database implementation
users = {
    "alex_l@gmail.com": {
        "name": "alex",
        "password": "secure password",
        "balance": 1000_000
    },
    "maria_l@gmail.com": {
        "name": "maria",
        "password": "very_secure password",
        "balance": 1000_000_000
    },
}


@app.get("/")
def index_page():
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    return Response(login_page, media_type="text/html")


@app.post("/login")
def get_success_login(email: str = Form(...), password: str = Form(...)):
    user = users.get(email)
    if not user or user["password"] != password:
        return Response("I don't know you", media_type="text/html")
    return Response(f"Your username: {user['name']}, password: {password}, balance: {user['balance']}",
                    media_type="text/html")
