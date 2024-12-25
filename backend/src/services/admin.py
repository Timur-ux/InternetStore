from sqlalchemy.orm import Session
from models.user import User
from models.buy import Buy
from db.session import get_session
from auth import hash_password


def get_all_users():
    """
    Получить список всех пользователей.
    """
    with get_session() as db:
        return db.query(User).all()


def delete_user_by_id(user_id: int):
    """
    Удалить пользователя по его ID.
    """
    with get_session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        db.delete(user)
        db.commit()


def get_sales_report():
    """
    Получить общий отчет по продажам.
    """
    with get_session() as db:
        return db.query(Buy).all()


def get_user_sales(user_id: int):
    """
    Получить продажи по пользователю.
    """
    with get_session() as db:
        return db.query(Buy).filter(Buy.user_id == user_id).all()


def add_user(login: str, password: str, access_level: int) -> User:
    """
    Добавить нового пользователя.
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
