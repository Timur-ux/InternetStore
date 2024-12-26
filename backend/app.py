from fastapi import FastAPI, Depends, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
import requests
import src.db.requests as db_requests
from src.db.sessionManager import SessionManager
from src.core.config import DB_CONFIG
import hashlib
import jwt
import datetime
import os

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

class BuyRequest(BaseModel):
    item_uris: List[str]

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

@app.post("/api/buy")
def buy(
    item_uris: BuyRequest,
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    """
    Покупка товаров. Считает общую стоимость и перенаправляет на сервис оплаты.
    Также добавляет запись о покупке в базу данных.
    """
    user = authenticate_user(token)  # already returns user info
    user_id = user["user_id"]

    # Получение товаров по URI
    items = db_requests.get_items_by_uris(sessionManager, item_uris.item_uris)
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")

    # Считаем стоимость и добавляем записи о покупке
    total_price = 0
    for item in items:
        item_id = item["id"]
        price = item["price"]
        cnt = item_uris.item_uris.count(str(item_id))  # количество товара в запросе
        total_price += price * cnt
        
        # Добавляем покупку в базу данных
        db_requests.add_purchase(sessionManager, user_id, item_id, price, cnt)

    # Логируем покупку
    db_requests.log_user_action(sessionManager, user_id, f"Purchased items: {item_uris.item_uris}")

    # Перенаправляем на сервис оплаты
    payment_service_url = os.getenv("PAYMENT_SERVICE_URL", "https://sber-payment-service.example.com/pay")
    response = requests.post(payment_service_url, json={"amount": total_price, "user_id": user_id})

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Payment service error")

    return {"message": "Purchase successful", "payment_status": response.json()}



@app.get("/api/recommendation")
def recommendation(
    n: int = Query(1, ge=1),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    """
    Получение списка рекомендованных товаров.
    """
    user = authenticate_user(token.credentials)
    user_id = user["user_id"]

    # Получаем рекомендации
    recommendations = db_requests.get_recommendations(sessionManager, user_id, n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")

    # Логируем запрос
    db_requests.log_user_action(sessionManager, user_id, f"Requested {n} recommendations")

    return recommendations


@app.get("/api/history")
def history(
    time: Optional[str] = None,
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    """
    Получение истории действий пользователей.
    """
    user = authenticate_user(token.credentials)
    if user["access_level"] < 2:  # Только администратор
        raise HTTPException(status_code=403, detail="Permission denied")

    start_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") if time else datetime.datetime.now() - datetime.timedelta(days=1)
    actions = db_requests.get_user_actions(sessionManager, start_time)

    return {"actions": actions}


@app.get("/api/selled")
def selled(
    time: Optional[str] = None,
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    """
    Получение списка проданных товаров.
    """
    user = authenticate_user(token.credentials)
    if user["access_level"] < 2:  # Только администратор
        raise HTTPException(status_code=403, detail="Permission denied")

    start_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") if time else datetime.datetime.now() - datetime.timedelta(days=1)
    selled_items = db_requests.get_selled_items(sessionManager, start_time)

    return {"selled_items": selled_items}


@app.get("/api/prediction")
def prediction(
    items: List[str],
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    """
    Получение предсказаний от сервиса нейросети.
    """
    user = authenticate_user(token.credentials)
    if user["access_level"] < 2:  # Только администратор
        raise HTTPException(status_code=403, detail="Permission denied")

    # Запрос к внешнему сервису предсказаний
    prediction_service_url = "http://neural-service.example.com/predict"
    response = requests.post(prediction_service_url, json={"items": items})

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Prediction service error")

    return {"predictions": response.json()}