from sqlalchemy.orm import Session
from models.user import User
from db.session import get_session
import bcrypt
import jwt
import datetime
from auth import hash_password

# ПЕРЕНЕСТИ В .env !!! 
SECRET_KEY = "your_super_secret_key"  # Рекомендуется хранить в переменных окружения


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
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def register_user(login: str, password: str, access_level: int) -> User:
    """
    Регистрация нового пользователя.
    """
    with get_session() as db:
        existing_user = db.query(User).filter(User.login == login).first()
        if existing_user:
            raise ValueError("User with this login already exists.")
        hashed_password = hash_password(password)
        new_user = User(login=login, password=hashed_password, access_level=access_level)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def authenticate_user(login: str, password: str) -> str:
    """
    Аутентификация пользователя.
    """
    with get_session() as db:
        user = db.query(User).filter(User.login == login).first()
        if not user or not verify_password(password, user.password):
            return None
        return generate_jwt(user.id, user.access_level)
