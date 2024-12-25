from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from models.buy import Buy


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
