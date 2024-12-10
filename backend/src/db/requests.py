import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor
import jwt
import bcrypt
import datetime

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

def create_user(sessionManager, login, password, access_level=1):
    """
    Создает нового пользователя с хешированным паролем.
    """
    hashed_password = hash_password(password)
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (login, password, access_level) VALUES (%s, %s, %s)",
                (login, hashed_password, access_level)
            )
            session.commit()

def authenticate_user(sessionManager, login, password):
    """
    Аутентифицирует пользователя по логину и паролю.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE login = %s",
                (login,)
            )
            user = cursor.fetchone()
            if user and verify_password(password, user["password"]):
                return generate_jwt(user["id"], user["access_level"])
            return None

def get_marks(sessionManager):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM marks")
            return cursor.fetchall()

def get_mark_by_id(sessionManager, mark_id):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM marks WHERE id = %s", (mark_id,))
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
