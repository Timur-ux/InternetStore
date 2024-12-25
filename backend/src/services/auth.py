from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from src.core.config import settings
import bcrypt
import jwt
import datetime


def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, hashed: str) -> bool:
    """
    Проверяет пароль с хешем.
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_jwt(user_id: int, access_level: int) -> str:
    """
    Генерация JWT токена.
    """
    payload = {
        "user_id": user_id,
        "access_level": access_level,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


async def register_user(session: AsyncSession, login: str, password: str, access_level: int) -> User:
    """
    Регистрация нового пользователя.
    """
    hashed_password = hash_password(password)
    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        raise ValueError("User with this login already exists.")

    new_user = User(login=login, password=hashed_password, access_level=access_level)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def authenticate_user(session: AsyncSession, login: str, password: str) -> str:
    """
    Аутентификация пользователя.
    """
    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user or not verify_password(password, user.password):
        return None
    return generate_jwt(user.id, user.access_level)
