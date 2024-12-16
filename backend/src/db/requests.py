import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor
import jwt
import bcrypt
import datetime

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
    Генерация JWT токена с SHA-256.
    """
    payload = {
        "user_id": user_id,
        "access_level": access_level,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token: str) -> dict:
    """
    Проверяет валидность JWT токена.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

import hashlib
from contextlib import closing

def create_user(sessionManager, login, password, access_level=1):
    # Хешируем пароль с использованием SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Открываем сессию с базой данных и выполняем запрос
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            # Вставляем нового пользователя с хешированным паролем
            cursor.execute(
                "INSERT INTO users (login, password, access_level) VALUES (%s, %s, %s)",
                (login, hashed_password, access_level)
            )
            # Сохраняем изменения в базе данных
            session.commit()

def authenticate_user(sessionManager, login, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE login = %s AND password = %s",
                (login, hashed_password)
            )
            user = cursor.fetchone()
            if user:
                token = jwt.encode(
                    {"user_id": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                    SECRET_KEY,
                    algorithm="HS256"
                )
                return token
            return None

def get_items(sessionManager):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT name, uri FROM items")
            return cursor.fetchall()
        
def get_item_by_id(sessionManager, item_id):
    """
    Получает информацию о товаре из базы данных по его идентификатору.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT name, uri, description, price, stock FROM items WHERE id = %s", (item_id,))
            return cursor.fetchone()

def add_mark(sessionManager, mark_id, mark_type, location_id, last_position):
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                "INSERT INTO marks (mark_id, mark_type, location_id, last_position) "
                "VALUES (%s, %s, %s, %s)",
                (mark_id, mark_type, location_id, last_position)
            )
            session.commit()

def update_mark(sessionManager, mark_id, mark_type, location_id, last_position):
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                "UPDATE marks SET mark_type = %s, location_id = %s, last_position = %s "
                "WHERE mark_id = %s",
                (mark_type, location_id, last_position, mark_id)
            )
            session.commit()

def delete_mark(sessionManager, mark_id):
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute("DELETE FROM marks WHERE id = %s", (mark_id,))
            session.commit()
