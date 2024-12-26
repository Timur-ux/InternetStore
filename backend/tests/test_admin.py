import pytest
from httpx import AsyncClient
from src.main import app
from src.dependencies.auth import get_user_type
from src.schemas.admin import ForecastRequest


@pytest.mark.asyncio
async def test_get_forecast_success(client: AsyncClient):
    async def override_get_user_type():
        return "administrator"

    app.dependency_overrides[get_user_type] = override_get_user_type

    payload = ForecastRequest(uris=["uri1", "uri2", "uri3"]).dict()
    response = await client.post("/api/v1/admin/forecast", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "forecast" in data
    assert isinstance(data["forecast"], list)

    del app.dependency_overrides[get_user_type]


@pytest.mark.asyncio
async def test_get_forecast_all_items(client: AsyncClient):
    async def override_get_user_type():
        return "administrator"

    app.dependency_overrides[get_user_type] = override_get_user_type

    payload = ForecastRequest(uris=None).dict()  # Запрашиваем прогноз для всех товаров
    response = await client.post("/api/v1/admin/forecast", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "forecast" in data
    assert isinstance(data["forecast"], list)

    del app.dependency_overrides[get_user_type]


@pytest.mark.asyncio
async def test_get_forecast_insufficient_permissions(client: AsyncClient):
    async def override_get_user_type():
        return "regular_user"

    app.dependency_overrides[get_user_type] = override_get_user_type

    payload = ForecastRequest(uris=["uri1", "uri2"]).dict()
    response = await client.post("/api/v1/admin/forecast", json=payload)
    
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Insufficient permissions"

    del app.dependency_overrides[get_user_type]


@pytest.mark.asyncio
async def test_get_forecast_invalid_service_response(client: AsyncClient, monkeypatch):
    async def mock_get_sales_forecast(item_uris=None):
        raise Exception("Failed to fetch forecast")

    async def override_get_user_type():
        return "administrator"

    app.dependency_overrides[get_user_type] = override_get_user_type

    from src.services.admin import get_sales_forecast
    monkeypatch.setattr("src.services.admin.get_sales_forecast", mock_get_sales_forecast)

    payload = ForecastRequest(uris=["uri1"]).dict()
    response = await client.post("/api/v1/admin/forecast", json=payload)
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Failed to fetch forecast"

    del app.dependency_overrides[get_user_type]
