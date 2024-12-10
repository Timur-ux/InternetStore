#!venv/bin/python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import src.db.requests as db_requests
from src.db.sessionManager import SessionManager
import src.db.sessionManager as sm
from src.db.requests import processAuth
from src.core.config import DB_CONFIG
import json
import jwt

sessionManager = sm.SessionManager(DB_CONFIG)

app = FastAPI()

origins = [
        "http://localhost:8080"
        ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_headers=['*'],
        allow_methods=['*'],
        )

class LoginModel(BaseModel):
    login: str
    password: str

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def index():
    response = {"data": "Hello world"}
    return json.dumps(response)

@app.post("/api/register")
def register(user: LoginModel):
    db_requests.create_user(sessionManager, user.login, user.password)
    return {"message": "User registered successfully"}

@app.get('/api/login')
def auth():
    # Do some auth login
    return "some auth data"

@app.get('/api/products')
def getProductList():
    # Do some get product list logic
    return "product list"
