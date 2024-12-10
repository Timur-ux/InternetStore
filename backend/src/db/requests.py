import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor
import hashlib
import jwt
import datetime

def processAuth(sessionManager: sm.SessionManager, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('select * from locations'); # for connection to db test
            return cursor.fetchall()

SECRET_KEY = "your_jwt_secret_key"

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

def get_products(sessionManager):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM products")
            return cursor.fetchall()

def get_product_by_id(sessionManager, product_id):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return cursor.fetchone()
        

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

# Функция для добавления новой марки
def add_mark(sessionManager, mark_id, mark_type, location_id, last_position):
    """
    Добавление новой записи в таблицу marks
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                "INSERT INTO marks (mark_id, mark_type, location_id, last_position) "
                "VALUES (%s, %s, %s, %s)",
                (mark_id, mark_type, location_id, last_position)
            )
            session.commit()

# Функция для обновления данных о марке
def update_mark(sessionManager, mark_id, mark_type, location_id, last_position):
    """
    Обновление данных о марке с указанным mark_id
    """
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
