import base64
import hashlib
import hmac
from typing import Optional

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_SIGN_KEY = "88e03b267580d15fc7e239e608a36e643cea2bf86c442b38c6d4b07dccd8d036"
PASSWORD_SALT = "257e7dfd5017ab0023150e46763a49543c672088f0a9dc18e4a0d69e79e42d1e"


def sign_data(data: str) -> str:
    """Return sign data"""
    return hmac.new(
        key=SECRET_SIGN_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_email_from_signed_string(email_signed: str) -> Optional[str]:
    email_base_64, sign = email_signed.split(".")
    email = base64.b64decode(email_base_64.encode()).decode()
    sign_for_validation = sign_data(email)
    if hmac.compare_digest(sign_for_validation, sign):
        return email


def verify_password(email: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash = hashlib.sha256((users[email]["password"] + PASSWORD_SALT).encode()).hexdigest().lower()
    return  password_hash == stored_password_hash


# simplified database implementation
users = {
    "alex_l@gmail.com": {
        "name": "alex",
        "password": "4e6965b2942bf58c3a60bb43e75a99b71d28caadae8d215088af390b3054977f",
        # hashlib.sha256(("secure password" + PASSWORD_SALT).encode()).hexdigest()
        "balance": 1000_000
    },
    "maria_l@gmail.com": {
        "name": "maria",
        "password": "60afe7edbbc5c8e37a591dc8e53ad441dcf670ef68b50c0a138dd3fd43e8c5b4",  # "very secure password"
        "balance": 1000_000_000
    },
}


@app.get("/")
def index_page(email: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()
    if not email:
        return Response(login_page, media_type="text/html")
    valid_email = get_email_from_signed_string(email)
    if not valid_email:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="email")
        return response
    try:
        users[valid_email]
    except KeyError:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="email")
        return response
    return Response(f"Hello, {valid_email}!", media_type="text/html")


@app.post("/login")
def get_success_login(email: str = Form(...), password: str = Form(...)):
    user = users.get(email)
    if not user or not verify_password(email, user["password"]):
        return Response("I don't know you", media_type="text/html")
    response = Response(f"Your username: {user['name']},</br> password: {password},</br> balance: {user['balance']}",
                        media_type="text/html")
    email_signed = base64.b64encode(email.encode()).decode() + "." + sign_data(email)
    response.set_cookie(key="email", value=email_signed)
    return response
