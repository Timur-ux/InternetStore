from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth import register_user, authenticate_user
from src.db.session import get_session
from src.dependencies.auth import get_user_type_by_token
from src.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Регистрация нового пользователя.
    """
    try:
        user = await register_user(session, payload.login, payload.password, 1)
        return RegisterResponse(message="User registered successfully", user_id=user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """
    Аутентификация пользователя. В ответе будет добавлен тип пользователя.
    """
    token = await authenticate_user(session, payload.login, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")

    # Устанавливаем JWT токен в cookies
    response.set_cookie(key="access_token", value=token, httponly=True)
    user_type = await get_user_type_by_token(token)
    return LoginResponse(message="Login successful", token=token, user_type=user_type)
