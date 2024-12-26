from src.services.balance import get_user_balance, top_up_balance
from fastapi import APIRouter, Depends, HTTPException, Cookie
from src.db.session import get_session
from src.services.purchase import process_purchase
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/user/balance", summary="Получить баланс пользователя")
async def get_balance(
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    try:
        balance = await get_user_balance(session, user_id)
        return {"balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/user/balance/top-up", summary="Пополнить баланс пользователя")
async def top_up(
    amount: float,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    try:
        payment_url = await top_up_balance(session, user_id, amount)
        return {"payment_url": payment_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/purchase", summary="Оформить покупку")
async def purchase_items(
    uris: List[str],
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user),
):
    try:
        await process_purchase(session, user_id, uris)
        return {"message": "Purchase successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))