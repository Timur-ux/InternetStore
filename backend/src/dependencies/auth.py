from fastapi import Depends, HTTPException, Cookie
from async_fastapi_jwt_auth import AuthJWT

def get_current_user(
    Authorize: AuthJWT = Depends(),
    access_token: str = Cookie(None)  # Получаем токен из cookie
) -> int:
    try:
        if access_token is None:
            raise HTTPException(status_code=401, detail="Token not found in cookies")
        
        Authorize.jwt_required()  # Проверка токена
        user_id = Authorize.get_jwt_subject()  # Получение идентификатора пользователя из токена
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(user_id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
