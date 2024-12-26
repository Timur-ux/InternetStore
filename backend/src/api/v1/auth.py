from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth import generate_jwt, register_user, authenticate_user
from src.db.session import get_session 
from src.dependencies.auth import get_user_type_by_token
from src.models.auth import AuthRequest

router = APIRouter()

@router.post("/register")
async def register(
    userData: AuthRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Регистрация нового пользователя.
    """
    try:
        # админа может добавлять только админ
        user = await register_user(session, userData.login, userData.password, 1)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(
    userData: AuthRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """
    Аутентификация пользователя. В ответе будет добавлен тип пользователя.
    """
    token = await authenticate_user(session, userData.login, userData.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    
    # Устанавливаем JWT токен в cookies
    response.set_cookie(key="access_token", value=token, httponly=True)
    user_type = await get_user_type_by_token(token)
    return {"message": "Login successful", "token": token, "user_type": user_type}

@router.post("/logout")
async def logout(
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """
    Выход из профиля. Ставим токен None с периодом жизни 5 секунд.
    """
    token = generate_jwt({}, timedelta(seconds=5))
    if not token:
        raise HTTPException(status_code=500, detail="Internal error")
    
    # Устанавливаем JWT токен в cookies
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Logout successful"}
