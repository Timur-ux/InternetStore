import pytest
from unittest.mock import MagicMock
from src.dependencies.auth import get_current_user_id

@pytest.mark.asyncio
async def test_get_balance(client, setup_database_with_data):
    # Предполагаем, что в базе данных уже есть пользователь с id 1 и баланс
    user_id = 1  # замените на id тестового пользователя

    # Переопределим функцию get_current_user_id для возврата test_user_id
    mock_get_current_user_id = MagicMock(return_value=user_id)
    client.app.dependency_overrides[get_current_user_id] = mock_get_current_user_id

    # Запрашиваем баланс пользователя
    response = await client.get("/api/v1/user/balance")
    
    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200
    
    # Проверяем, что баланс есть в ответе
    data = response.json()
    assert "balance" in data
    assert isinstance(data["balance"], (float, int))

# @pytest.mark.asyncio
# async def test_top_up_balance(client, setup_database_with_data):
#     # Тестируем пополнение баланса
#     user_id = 1  # замените на id тестового пользователя
#     amount = 100.0  # Сумма пополнения

#     # Переопределим функцию get_current_user_id для возврата test_user_id
#     mock_get_current_user_id = MagicMock(return_value=user_id)
#     client.app.dependency_overrides[get_current_user_id] = mock_get_current_user_id

#     # Отправляем запрос на пополнение баланса
#     response = await client.post("/api/v1/user/balance/top-up", json={"amount": amount})

#     # Проверяем, что запрос прошел успешно
#     assert response.status_code == 200
    
#     # Проверяем, что в ответе присутствует payment_url
#     data = response.json()
#     assert "payment_url" in data
#     assert isinstance(data["payment_url"], str)  # Проверяем, что payment_url - строка

# @pytest.mark.asyncio
# async def test_purchase_items(client, setup_database_with_data):
#     # Тестируем оформление покупки
#     user_id = 1  # замените на id тестового пользователя
#     uris = ["http://example.com/item/1", "http://example.com/item/2"]  # Тестовые URI товаров

#     # Переопределим функцию get_current_user_id для возврата test_user_id
#     mock_get_current_user_id = MagicMock(return_value=user_id)
#     client.app.dependency_overrides[get_current_user_id] = mock_get_current_user_id

#     # Отправляем запрос на оформление покупки
#     response = await client.post("/api/v1/purchase", json=uris)

#     # Проверяем, что запрос прошел успешно
#     assert response.status_code == 200

#     # Проверяем, что в ответе есть сообщение об успешной покупке
#     data = response.json()
#     assert "message" in data
#     assert data["message"] == "Purchase successful"
