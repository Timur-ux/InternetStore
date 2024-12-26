import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import ASGITransport, AsyncClient
from src.models.base import Base
from src.models.item import Item
from src.models.shop import Shop
from src.main import app
from src.db.session import get_session

# Создаем тестовый движок SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
TestingSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="function")
async def setup_database():
    """
    Подготовка тестовой базы данных.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def setup_database_with_data(setup_database):
    """
    Фикстура для добавления данных в тестовую базу перед тестами.
    """
    async with TestingSessionLocal() as session:
        # Создаем тестовые магазины
        shop1 = Shop(shop_name="Shop 1")
        shop2 = Shop(shop_name="Shop 2")
        shop3 = Shop(shop_name="Shop 3")
        session.add_all([shop1, shop2, shop3])
        await session.commit()

        item1 = Item(
            item_name="Item 1", 
            item_price=100.0, 
            uri="uri1", 
            item_category_id=1,
            item_category_name="Category 1"
        )
        item2 = Item(
            item_name="Item 2", 
            item_price=150.0, 
            uri="uri2", 
            item_category_id=1,  
            item_category_name="Category 1"
        )
        item3 = Item(
            item_name="Item 3", 
            item_price=200.0, 
            uri="uri3", 
            item_category_id=2, 
            item_category_name="Category 2"
        )

        # Связываем товары с магазинами
        item1.shops.append(shop1)
        item1.shops.append(shop2)
        item2.shops.append(shop2)
        item2.shops.append(shop3)
        item3.shops.append(shop1)

        session.add_all([item1, item2, item3])
        await session.commit()

    yield  # После выполнения тестов фикстура вернет управление обратно

    # Очистка базы данных после тестов
    async with TestingSessionLocal() as session:
        await session.execute("DELETE FROM item_shop") 
        await session.execute("DELETE FROM item")  
        await session.execute("DELETE FROM shop") 
        await session.execute("DELETE FROM users")
        await session.commit()

@pytest.fixture
async def client(setup_database):
    """
    Переопределяем get_session и создаем тестовый клиент.
    """
    async def override_get_session():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
