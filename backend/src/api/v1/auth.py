from fastapi import APIRouter, Depends, HTTPException
from services.auth import register_user, authenticate_user

router = APIRouter()

@router.post("/register")
def register(login: str, password: str, access_level: int):
    """
    Регистрация нового пользователя.
    """
    try:
        user = register_user(login, password, access_level)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(login: str, password: str):
    """
    Аутентификация пользователя.
    """
    token = authenticate_user(login, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {"token": token}
