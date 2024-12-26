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
def decode_jwt(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        return int(user_id)
    except PyJWTError:
        return None

# Функция для получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    user_id = decode_jwt(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
