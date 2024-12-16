from fastapi import FastAPI, Depends, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import List
import src.db.requests as db_requests
from src.db.sessionManager import SessionManager
from src.core.config import DB_CONFIG
import hashlib
import jwt
import datetime

sessionManager = SessionManager(DB_CONFIG)
app = FastAPI()

# ПЕРЕНЕСТИ В .env !!! 
SECRET_KEY = "your_super_secret_key"

# CORS settings
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        return db_requests.verify_jwt(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# Models
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
    last_position: List[float]

@app.get("/")
def index():
    return {"message": "Welcome to the Internet Store API"}

@app.post("/api/register")
def register(
    user: RegModel, authorization: str = Header(None)
):
    """
    Регистрация пользователя. Если токен отсутствует, создаётся обычный пользователь с уровнем доступа 1.
    Только администраторы могут создавать других администраторов.
    """
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    token = authorization.split(" ")[1]
    # Если создаётся администратор, проверяем права текущего пользователя
    if user.access_level == 2:
        try:
            # Проверяем токен
            decoded_token = db_requests.verify_jwt(token)
            print(decoded_token)  # Здесь вы можете использовать декодированный токен
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
        # current_access_level = current_user.get("access_level")
        # if current_access_level != 2:
        #     raise PermissionError("Only administrators can create other administrators")

            
    # Выполняем создание пользователя
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


@app.get("/api/items", dependencies=[Depends(authenticate_user)])
def list_marks():
    return {"items": db_requests.get_items(sessionManager)}


@app.get("/api/item")
def get_item(id: int = Query(..., description=[Depends(authenticate_user)])):
    """
    Получение полной информации о товаре по его идентификатору.
    """
    item = db_requests.get_item_by_id(id)  # Вызов функции для получения данных из базы
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": item}