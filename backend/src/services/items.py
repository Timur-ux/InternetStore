from sqlalchemy.orm import Session
from models.item import Item
from db.session import get_session


def get_all_items():
    """
    Получить список всех товаров.
    """
    with get_session() as db:
        return db.query(Item).all()


def get_item(item_id: int):
    """
    Получить информацию о товаре по его ID.
    """
    with get_session() as db:
        return db.query(Item).filter(Item.id == item_id).first()


def create_item(item_data: dict):
    """
    Добавить новый товар.
    """
    with get_session() as db:
        new_item = Item(**item_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item


def delete_item(item_id: int):
    """
    Удалить товар по его ID.
    """
    with get_session() as db:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        db.delete(item)
        db.commit()
