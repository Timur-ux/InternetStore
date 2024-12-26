from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import User
from src.models.buy import Buy
import httpx
from typing import List, Optional

async def get_all_users(session: AsyncSession):
    """
    Получить список всех пользователей.
    """
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_user_by_id(session: AsyncSession, user_id: int):
    """
    Удалить пользователя по его ID.
    """
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise ValueError("User not found")
    await session.delete(user)
    await session.commit()


async def get_sales_report(session: AsyncSession):
    """
    Получить общий отчет по продажам.
    """
    stmt = select(Buy)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_sales(session: AsyncSession, user_id: int):
    """
    Получить продажи по пользователю.
    """
    stmt = select(Buy).where(Buy.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()



async def get_sales_forecast(item_uris: Optional[List[str]] = None):
    url = "http://forecast_service_url/predict"  # Здесь указываем адрес сервиса прогнозирования
    payload = {}

    if item_uris:
        payload['item_uris'] = item_uris
    else:
        # Если не передан ни список товаров, ни URI, делаем прогноз для всех товаров
        payload['all_items'] = True

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        
    if response.status_code != 200:
        raise Exception(f"Failed to fetch forecast: {response.text}")
    
    return response.json()  # Предполагаем, что возвращается JSON с прогнозом
