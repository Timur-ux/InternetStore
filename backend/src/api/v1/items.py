from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.services.items import get_all_items, get_items_by_uris
from src.db.session import get_session

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