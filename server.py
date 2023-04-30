from typing import Optional

from fastapi import FastAPI, Form, Cookie
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
def index_page(email: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    if email:
        try:
            users[email]['name']
        except KeyError:
            response = Response(login_page, media_type="text/html")
            response.delete_cookie(key="email")
            return response
        return Response(f"Hello, {users[email]['name']}!", media_type="text/html")
    return Response(login_page, media_type="text/html")


@app.post("/login")
def get_success_login(email: str = Form(...), password: str = Form(...)):
    user = users.get(email)
    if not user or user["password"] != password:
        return Response("I don't know you", media_type="text/html")
    response = Response(f"Your username: {user['name']},</br> password: {password},</br> balance: {user['balance']}",
                    media_type="text/html")
    response.set_cookie(key="email", value=email)
    return response
