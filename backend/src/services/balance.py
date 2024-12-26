from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.models.user import User
from decimal import Decimal

async def get_user_balance(session: AsyncSession, user_id: int) -> float:
    user = await session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    return user.balance

async def top_up_balance(session: AsyncSession, user_id: int, amount: float) -> float:
    """
    Пополнение баланса пользователя в базе данных.
    """
    # Получаем текущий баланс пользователя
    user = await session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    # Обновляем баланс 
    new_balance = user.balance + Decimal(amount) 
    stmt = update(User).where(User.id == user_id).values(balance=new_balance)
    await session.execute(stmt)
    await session.commit()

    return new_balance