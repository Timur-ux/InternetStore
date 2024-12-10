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

class RegModel(BaseModel):
    login: str
    password: str
    access_level: int 

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
def register(user: RegModel):
    try:
        db_requests.create_user(sessionManager, user.login, user.password, user.access_level)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

@app.post("/api/login")
def login(user: LoginModel):
    token = db_requests.authenticate_user(sessionManager, user.login, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {"token": token}

@app.get('/api/products')
def getProductList():
    # Do some get product list logic
    return "product list"
