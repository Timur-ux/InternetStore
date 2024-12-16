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
            # Проверяем, существует ли пользователь с таким логином
            cursor.execute("SELECT COUNT(*) FROM users WHERE login = %s", (login,))
            count = cursor.fetchone()[0]
            
            # Если пользователь уже существует, выбрасываем исключение
            if count > 0:
                raise ValueError(f"User with login '{login}' already exists.")

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
            cursor.execute("SELECT name, uri FROM item")
            return cursor.fetchall()
        
def get_item_by_id(sessionManager, item_id):
    """
    Получает информацию о товаре из базы данных по его идентификатору.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT name, uri, description, price, stock FROM item WHERE id = %s", (item_id,))
            return cursor.fetchone()

# Логирование действий пользователя
def log_user_action(sessionManager, user_id: int, action: str):
    """
    Логирует действия пользователя с текущим временем.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user_action (user_id, action) VALUES (%s, %s)",
                (user_id, action)
            )
            session.commit()

# Получение списка товаров по URI
def get_items_by_uris(sessionManager, item_uris: list):
    """
    Получение информации о товарах по списку URI.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT id, name, price FROM item WHERE uri::text = ANY(%s)",
                (item_uris,)
            )
            return cursor.fetchall()

# Получение рекомендаций на основе покупок
def get_recommendations(sessionManager, user_id: int, n: int):
    """
    Генерация списка рекомендованных товаров на основе покупок текущего пользователя.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT DISTINCT i.id, i.name, i.price
                FROM buy b1
                JOIN buy b2 ON b1.item_id = b2.item_id
                JOIN item i ON b2.item_id = i.id
                WHERE b1.user_id = %s AND b2.user_id != %s
                LIMIT %s
                """,
                (user_id, user_id, n)
            )
            return cursor.fetchall()


# Получение истории действий пользователей
def get_user_actions(sessionManager, start_time: datetime.datetime):
    """
    Получение истории действий пользователей.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT user_id, action, action_time
                FROM user_action
                WHERE action_time >= %s
                ORDER BY action_time DESC
                """,
                (start_time,)
            )
            return cursor.fetchall()

# Получение проданных товаров
def get_selled_items(sessionManager, start_time: datetime.datetime):
    """
    Получение списка проданных товаров с момента start_time.
    """
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT i.id, i.name, i.price, b.buy_time
                FROM item i
                JOIN buy b ON i.id = b.item_id
                WHERE b.buy_time >= %s
                ORDER BY b.buy_time DESC
                """,
                (start_time,)
            )
            return cursor.fetchall()
        


def add_purchase(sessionManager, user_id: int, item_id: int, price: float, cnt: int):
    """
    Добавляет запись о покупке в таблицу buy.
    
    :param sessionManager: Менеджер сессий для подключения к базе данных
    :param user_id: Идентификатор пользователя
    :param item_id: Идентификатор товара
    :param price: Цена товара
    :param cnt: Количество товара
    """
    # Получаем текущую дату и время для записи в поле buy_time
    buy_time = datetime.datetime.now()
    
    # Открываем сессию с базой данных и выполняем запрос
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO buy (user_id, price, cnt, buy_time)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, price, cnt, buy_time)
            )
            return cursor.fetchall()