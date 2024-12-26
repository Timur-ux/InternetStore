# test_auth.py
import pytest
from fastapi.testclient import TestClient
from src.models.user import User
from src.db.session_test import get_session_test, cleanup  # Импортируем сессию и очистку

@pytest.mark.asyncio
async def test_register_user(client: TestClient):
    """
    Тест на регистрацию нового пользователя
    """
    login = "test1"
    password = "test1"

    # Отправляем запрос на регистрацию
    response = client.post("/api/v1/register", params={"login": login, "password": password})
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert "user_id" in data
    
    # Получаем сессию для работы с тестовой базой
    db = next(get_session_test())
    
    # Проверка, что пользователь был создан в базе данных
    user_id = data["user_id"]
    user = db.query(User).filter(User.id == user_id).first()  # Используем синхронный запрос для тестов
    assert user is not None
    assert user.login == login

    # Очистка базы данных после теста
    cleanup()

