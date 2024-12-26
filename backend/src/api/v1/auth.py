from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth import register_user, authenticate_user
from src.db.session import get_session 
router = APIRouter()

@router.post("/register")
async def register(
    login: str, 
    password: str, 
    session: AsyncSession = Depends(get_session)
):
    """
    Регистрация нового пользователя.
    """
    try:
        # админа может добавлять только админ
        user = await register_user(session, login, password, 1)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(
    login: str, 
    password: str, 
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    """
    Аутентификация пользователя.
    """
    token = await authenticate_user(session, login, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    
    response.set_cookie(key="access_token", value=token, httponly=True)
    
    return {"message": "Login successful", "token": token}
