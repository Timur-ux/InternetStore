from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from models.item import Item
from models.shop import Shop

async def get_all_items(session: AsyncSession) -> List[dict]:
    """
    Получает список всех товаров с детальной информацией.
    """
    result = await session.execute(
        select(Item).options(
            selectinload(Item.shops),  # Предзагрузка связанных магазинов
        )
    )
    items = result.scalars().all()
    return [
        {
            "id": item.item_id,
            "name": item.item_name,
            "uri": item.uri,
            "shops": [
                {
                    "shop_id": shop.shop_id,
                    "shop_name": shop.shop_name,
                    # Если цена хранится в промежуточной таблице, нужно добавить соответствующее поле
                    # "price": shop.price,  # Убедитесь, что у вас есть поле price в промежуточной таблице
                }
                for shop in item.shops
            ],
            "price": item.item_price,
        }
        for item in items
    ]

async def get_items_by_uris(session: AsyncSession, uris: List[str]) -> List[dict]:
    """
    Получение данных о товарах по списку URI.
    """
    result = await session.execute(
        select(Item).options(
            selectinload(Item.shops)  # Предзагрузка связанных магазинов
        ).where(Item.uri.in_(uris))
    )
    items = result.scalars().all()
    return [
        {
            "id": item.item_id,
            "name": item.item_name,
            "uri": item.uri,
            "shops": [
                {
                    "shop_id": shop.shop_id,
                    "shop_name": shop.shop_name,
                    # "price": shop.price,  # Убедитесь, что у вас есть поле price в промежуточной таблице
                }
                for shop in item.shops
            ],
        }
        for item in items
    ]


# async def get_item(session: AsyncSession, item_id: int):
#     """
#     Получить информацию о товаре по его ID.
#     """
#     stmt = select(Item).where(Item.id == item_id)
#     result = await session.execute(stmt)
#     return result.scalars().first()


# async def create_item(session: AsyncSession, item_data: dict):
#     """
#     Добавить новый товар.
#     """
#     new_item = Item(**item_data)
#     session.add(new_item)
#     await session.commit()
#     await session.refresh(new_item)
#     return new_item


# async def delete_item(session: AsyncSession, item_id: int):
#     """
#     Удалить товар по его ID.
#     """
#     stmt = select(Item).where(Item.id == item_id)
#     result = await session.execute(stmt)
#     item = result.scalars().first()

#     if not item:
#         raise ValueError("Item not found")
#     await session.delete(item)
#     await session.commit()
