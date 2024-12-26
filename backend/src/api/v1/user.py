from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.services.balance import get_user_balance, top_up_balance
from src.services.purchase import process_purchase
from src.db.session import get_session
from src.dependencies.auth import get_current_user_id
from src.schemas.user import (
    BalanceResponse,
    TopUpRequest,
    TopUpResponse,
    PurchaseRequest,
    PurchaseResponse,
)

router = APIRouter()

@router.get(
    "/user/balance",
    summary="Получить баланс пользователя",
    response_model=BalanceResponse,
)
async def get_balance(
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    try:
        balance = await get_user_balance(session, user_id)
        return {"balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/user/balance/top-up",
    summary="Пополнить баланс пользователя",
    response_model=TopUpResponse,
)
async def top_up(
    request: TopUpRequest,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    try:
        new_balance = await top_up_balance(session, user_id, request.amount)
        return {"new_balance": new_balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/purchase",
    summary="Оформить покупку",
    response_model=PurchaseResponse,
)
async def purchase_items(
    request: PurchaseRequest,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    try:
        await process_purchase(session, user_id, request.uris)
        return {"message": "Purchase successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
