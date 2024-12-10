#!venv/bin/python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import src.db.requests as db_requests
from src.db.sessionManager import SessionManager
import src.db.sessionManager as sm
from src.db.requests import processAuth
from src.core.config import DB_CONFIG
import json
import jwt
from src.db.requests import (
    get_marks, get_mark_by_id, add_mark, update_mark, delete_mark
)

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

class Mark(BaseModel):
    mark_id: int
    mark_type: int
    location_id: int
    last_position: List[float]  # Это будет список с 3 float значениями

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

@app.get("/api/marks")
def list_marks():
    return {"marks": get_marks(sessionManager)}

@app.get("/api/marks/{mark_id}")
def get_mark(mark_id: int):
    mark = get_mark_by_id(sessionManager, mark_id)
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    return mark

@app.put("/api/marks/{mark_id}")
def create_mark(mark_id: int, mark: Mark):
    try:
        # Вставляем данные марки в базу данных
        add_mark(sessionManager, mark.mark_id, mark.mark_type, mark.location_id, mark.last_position)
        return {"message": "Mark created successfully"}
    except Exception as e:
        # Возвращаем ошибку, если что-то пошло не так
        raise HTTPException(status_code=500, detail=f"Error creating mark: {str(e)}")


def modify_mark(mark_id: int, mark: Mark):
    """
    Эндпоинт для обновления данных о марке.
    
    Args:
        mark_id (int): Идентификатор марки для обновления.
        mark (Mark): Данные марки, включая тип, местоположение и последнюю позицию.
    
    Returns:
        dict: Подтверждение успешного обновления.
    """
    try:
        update_mark(sessionManager, mark_id, mark.mark_type, mark.location_id, mark.last_position)
        return {"message": "Mark updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/marks/{mark_id}")
def remove_mark(mark_id: int):
    delete_mark(sessionManager, mark_id)
    return {"message": "Mark deleted successfully"}