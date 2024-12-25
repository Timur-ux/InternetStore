from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.item import Item


async def get_all_items(session: AsyncSession):
    """
    Получить список всех товаров.
    """
    stmt = select(Item)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_item(session: AsyncSession, item_id: int):
    """
    Получить информацию о товаре по его ID.
    """
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_item(session: AsyncSession, item_data: dict):
    """
    Добавить новый товар.
    """
    new_item = Item(**item_data)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item


async def delete_item(session: AsyncSession, item_id: int):
    """
    Удалить товар по его ID.
    """
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalars().first()

    if not item:
        raise ValueError("Item not found")
    await session.delete(item)
    await session.commit()
