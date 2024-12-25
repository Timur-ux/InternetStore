from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from services.items import get_all_items, get_items_by_uris
from db.session import get_session

router = APIRouter()

@router.get("/items", summary="Получить список всех товаров")
async def fetch_all_items(session: AsyncSession = Depends(get_session)):
    try:
        items = await get_all_items(session)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/items/list", summary="Получить данные о товарах по URI")
async def fetch_items_by_uri(
    uris: List[str], session: AsyncSession = Depends(get_session)
):
    try:
        items = await get_items_by_uris(session, uris)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.get("/items/{item_id}")
# def retrieve_item(item_id: int):
#     """
#     Получить информацию о товаре по его идентификатору.
#     """
#     try:
#         item = get_item(item_id)
#         if not item:
#             raise HTTPException(status_code=404, detail="Item not found")
#         return item
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/items")
# def add_item(item_data: dict):
#     """
#     Добавить новый товар.
#     """
#     try:
#         return create_item(item_data)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.delete("/items/{item_id}")
# def remove_item(item_id: int):
#     """
#     Удалить товар по его идентификатору.
#     """
#     try:
#         delete_item(item_id)
#         return {"message": "Item deleted successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
