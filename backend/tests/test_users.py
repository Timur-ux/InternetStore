import pytest
from src.dependencies.auth import get_current_user_id
from src.main import app

@pytest.mark.asyncio
async def test_get_balance(client, setup_database_with_data):
    user_id = 1

    # Переопределим функцию get_current_user_id для возврата test_user_id
    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    # Запрашиваем баланс пользователя
    response = await client.get("/api/v1/user/balance")
    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200
    
    # Проверяем, что баланс есть в ответе
    data = response.json()
    assert "balance" in data
    assert isinstance(data["balance"], (float, int))

    # Удаляем переопределение после теста
    del app.dependency_overrides[get_current_user_id]


@pytest.mark.asyncio
async def test_top_up_balance(client, setup_database_with_data):
    user_id = 1
    amount_to_top_up = 50.0

    # Переопределим функцию get_current_user_id для возврата test_user_id
    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    # Пополняем баланс пользователя
    response = await client.post("/api/v1/user/balance/top-up", params={"amount": amount_to_top_up})
    
    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200
    
    # Проверяем, что в ответе есть payment_url
    data = response.json()
    assert "payment_url" in data

    # Удаляем переопределение после теста
    del app.dependency_overrides[get_current_user_id]


@pytest.mark.asyncio
async def test_purchase_items(client, setup_database_with_data):
    user_id = 1
    uris_to_purchase = ["uri1", "uri2"]

    # Переопределим функцию get_current_user_id для возврата test_user_id
    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    # Оформляем покупку
    response = await client.post("/api/v1/purchase", json=uris_to_purchase)
    print(response.json())
    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200
    
    # Проверяем, что в ответе есть сообщение об успешной покупке
    data = response.json()
    assert "message" in data
    assert data["message"] == "Purchase successful"

    # Удаляем переопределение после теста
    del app.dependency_overrides[get_current_user_id]


@pytest.mark.asyncio
async def test_purchase_items_insufficient_balance(client, setup_database_with_data):
    user_id = 1
    uris_to_purchase = ["uri1", "uri2", "uri3"]  # Три URI для покупки

    # Переопределим функцию get_current_user_id для возврата test_user_id
    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    # Пытаемся оформить покупку
    response = await client.post("/api/v1/purchase", json=uris_to_purchase)
    
    # Проверяем, что запрос вернул ошибку
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Insufficient balance"

    # Удаляем переопределение после теста
    del app.dependency_overrides[get_current_user_id]