import pytest

@pytest.mark.asyncio
async def test_fetch_all_items(client):
    # Запрос на получение всех товаров
    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)  # Ожидаем список товаров

@pytest.mark.asyncio
async def test_fetch_items_by_uri(client):
    # Предполагаем, что товары с этими URI существуют
    uris = ["uri1", "uri2", "uri3"]
    response = await client.post("/api/v1/items/list", json=uris)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)  # Ожидаем список товаров

@pytest.mark.asyncio
async def test_fetch_items_by_invalid_uri(client):
    # Пытаемся запросить товары по несуществующим URI
    uris = ["invalid_uri1", "invalid_uri2"]
    response = await client.post("/api/v1/items/list", json=uris)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data['items'] == []

@pytest.mark.asyncio
async def test_fetch_all_items_empty(client):
    # Тестируем случай, когда нет товаров в базе данных
    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data['items'] == []

@pytest.mark.asyncio
async def test_fetch_items_by_uri_empty(client):
    # Запрос товаров по пустому списку URI
    response = await client.post("/api/v1/items/list", json=[])
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["items"] == []  # Ожидаем пустой список товаров
