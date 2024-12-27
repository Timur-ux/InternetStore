from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from datetime import datetime
from typing import Optional
from src.core.config import settings

# Секретный ключ и алгоритм для подписи токенов
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

# Функция для декодирования JWT токена
def decode_jwt(token: str) -> Optional[dict]:
    """
    Декодирует JWT токен и извлекает информацию о пользователе (user_id, access_level).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        access_level = payload.get("access_level")
        
        if user_id is None or access_level is None:
            return None
        
        return {"user_id": user_id, "access_level": access_level}
    
    except PyJWTError:
        return None
    
# Функция для получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Получает информацию о текущем пользователе на основе JWT токена.
    Возвращает словарь с 'user_id' и 'access_level'.
    """
    user_data = decode_jwt(token)
    
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_data

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Получает информацию о текущем пользователе на основе JWT токена.
    Возвращает словарь с 'user_id' и 'access_level'.
    """
    user_data = decode_jwt(token)
    
    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_data["user_id"]

# Функция для получения типа пользователя (рядовой пользователь/администратор)
async def get_user_type(current_user: dict = Depends(get_current_user)) -> str:
    """
    Определяет тип пользователя в зависимости от уровня доступа.
    Возвращает 'Администратор' или 'Рядовой пользователь'.
    """
    if current_user["access_level"] >= 2:
        return "Администратор"
    return "Рядовой пользователь"

async def get_user_type_by_token(token: str) -> str:
    """
    Определяет тип пользователя в зависимости от уровня доступа.
    Возвращает 'Администратор' или 'Рядовой пользователь'.
    """
    current_user = decode_jwt(token)
    if current_user["access_level"] >= 2:
        return "Администратор"
    return "Рядовой пользователь"
