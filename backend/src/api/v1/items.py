from fastapi import APIRouter, HTTPException
from services.items import get_all_items, get_item, create_item, delete_item

router = APIRouter()

@router.get("/items")
def list_items():
    """
    Получить список всех товаров.
    """
    try:
        return get_all_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/items/{item_id}")
def retrieve_item(item_id: int):
    """
    Получить информацию о товаре по его идентификатору.
    """
    try:
        item = get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/items")
def add_item(item_data: dict):
    """
    Добавить новый товар.
    """
    try:
        return create_item(item_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/items/{item_id}")
def remove_item(item_id: int):
    """
    Удалить товар по его идентификатору.
    """
    try:
        delete_item(item_id)
        return {"message": "Item deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
