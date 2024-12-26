import pytest

@pytest.mark.asyncio
async def test_register(client):
    # Успешная регистрация
    response = await client.post(
        "/api/v1/register", params={"login": "testuser", "password": "testpassword"}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


@pytest.mark.asyncio
async def test_login(client):
    # Регистрация пользователя
    await client.post(
        "/api/v1/register", params={"login": "testuser", "password": "testpassword"}
    )
    # Логин пользователя
    response = await client.post(
        "/api/v1/login", params={"login": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["message"] == "Login successful"


@pytest.mark.asyncio
async def test_register_existing_user(client):
    # Регистрация пользователя
    await client.post(
        "/api/v1/register", params={"login": "testuser", "password": "testpassword"}
    )
    
    # Пытаться зарегистрировать того же пользователя
    response = await client.post(
        "/api/v1/register", params={"login": "testuser", "password": "newpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this login already exists."


@pytest.mark.asyncio
async def test_login_invalid_password(client):
    # Регистрация пользователя
    await client.post(
        "/api/v1/register", params={"login": "testuser", "password": "testpassword"}
    )
    
    # Логин с неправильным паролем
    response = await client.post(
        "/api/v1/login", params={"login": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login or password"


@pytest.mark.asyncio
async def test_login_non_existing_user(client):
    # Пытаться залогиниться с несуществующим пользователем
    response = await client.post(
        "/api/v1/login", params={"login": "nonexistentuser", "password": "testpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login or password"
