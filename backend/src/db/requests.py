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

def create_user(sessionManager, login, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with closing(sessionManager.createSession()) as session:
        with session.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (login, password) VALUES (%s, %s)",
                (login, hashed_password)
            )
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