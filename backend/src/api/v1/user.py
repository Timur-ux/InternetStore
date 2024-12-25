from services.balance import get_user_balance, top_up_balance
from fastapi import APIRouter, Depends, HTTPException
from db.session import get_session
from services.purchase import process_purchase
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


router = APIRouter()

@router.get("/user/balance", summary="Получить баланс пользователя")
async def get_balance(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        balance = await get_user_balance(session, user_id)
        return {"balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/balance/top-up", summary="Пополнить баланс пользователя")
async def top_up(user_id: int, amount: float):
    try:
        payment_url = await top_up_balance(user_id, amount)
        return {"payment_url": payment_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/purchase", summary="Оформить покупку")
async def purchase_items(
    uris: List[str], user_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        await process_purchase(session, user_id, uris)
        return {"message": "Purchase successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))