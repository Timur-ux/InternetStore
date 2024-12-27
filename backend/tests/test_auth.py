import pytest
from httpx import AsyncClient
from src.schemas.auth import RegisterRequest, LoginRequest


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    # Успешная регистрация
    payload = RegisterRequest(login="testuser", password="testpassword").dict()
    response = await client.post("/api/v1/register", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert "user_id" in data


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    # Регистрация пользователя
    register_payload = RegisterRequest(login="testuser", password="testpassword").dict()
    await client.post("/api/v1/register", json=register_payload)
    
    # Логин пользователя
    login_payload = LoginRequest(login="testuser", password="testpassword").dict()
    response = await client.post("/api/v1/login", json=login_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["message"] == "Login successful"


@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient):
    # Регистрация пользователя
    register_payload = RegisterRequest(login="testuser", password="testpassword").dict()
    await client.post("/api/v1/register", json=register_payload)
    
    # Попытка повторной регистрации с тем же логином
    response = await client.post("/api/v1/register", json=register_payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "User with this login already exists."


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    # Регистрация пользователя
    register_payload = RegisterRequest(login="testuser", password="testpassword").dict()
    await client.post("/api/v1/register", json=register_payload)
    
    # Попытка логина с неправильным паролем
    login_payload = LoginRequest(login="testuser", password="wrongpassword").dict()
    response = await client.post("/api/v1/login", json=login_payload)
    
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid login or password"


@pytest.mark.asyncio
async def test_login_non_existing_user(client: AsyncClient):
    # Попытка логина с несуществующим пользователем
    login_payload = LoginRequest(login="nonexistentuser", password="testpassword").dict()
    response = await client.post("/api/v1/login", json=login_payload)
    
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid login or password"
