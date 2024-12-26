import pytest
from httpx import AsyncClient
from src.schemas.items import ItemsByUriRequest


@pytest.mark.asyncio
async def test_fetch_all_items(client: AsyncClient, setup_database_with_data):
    # Запрос на получение всех товаров
    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)  # Ожидаем список товаров


@pytest.mark.asyncio
async def test_fetch_items_by_uri(client: AsyncClient, setup_database_with_data):
    # Предполагаем, что товары с этими URI существуют
    payload = ItemsByUriRequest(uris=["uri1", "uri2", "uri3"]).dict()
    response = await client.post("/api/v1/items/list", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)  # Ожидаем список товаров


@pytest.mark.asyncio
async def test_fetch_items_by_invalid_uri(client: AsyncClient, setup_database_with_data):
    # Пытаемся запросить товары по несуществующим URI
    payload = ItemsByUriRequest(uris=["invalid_uri1", "invalid_uri2"]).dict()
    response = await client.post("/api/v1/items/list", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data['items'] == []


@pytest.mark.asyncio
async def test_fetch_items_by_uri_empty(client: AsyncClient, setup_database_with_data):
    # Запрос товаров по пустому списку URI
    payload = ItemsByUriRequest(uris=[]).dict()
    response = await client.post("/api/v1/items/list", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["items"] == []  # Ожидаем пустой список товаров
