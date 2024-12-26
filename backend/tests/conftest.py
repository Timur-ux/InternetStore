import pytest
from src.main import app
from fastapi.testclient import TestClient
import pytest
from fastapi.testclient import TestClient
from src.db.session_test import get_session_test, cleanup, SessionLocal


# Фикстура для создания базы данных для тестов
@pytest.fixture(scope="module")
def test_db():
    # Используем тестовую сессию
    db = next(get_session_test())  # Получаем сессию из get_session_test
    yield db
    # Очистка базы данных после тестов
    cleanup()

# Фикстура для клиента FastAPI
@pytest.fixture(scope="module")
def client(test_db):
    app.dependency_overrides[SessionLocal] = lambda: test_db
    client = TestClient(app)
    yield client