from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.models.buy import Buy
from src.models.user import User
from typing import List
from sqlalchemy import select

async def process_purchase(session: AsyncSession, user_id: int, uris: List[str]):
    """
    Оформляет покупку товаров.
    """
    result = await session.execute(
        select(Item).where(Item.uri.in_(uris))
    )
    items = result.scalars().all()

    if not items:
        raise ValueError("Items not found")

    total_cost = sum(item.price for item in items)
    user = await session.get(User, user_id)

    if not user or user.balance < total_cost:
        raise ValueError("Insufficient balance")

    user.balance -= total_cost

    for item in items:
        buy = Buy(user_id=user.id, item_id=item.id, price=item.price, cnt=1)
        session.add(buy)

    await session.commit()
