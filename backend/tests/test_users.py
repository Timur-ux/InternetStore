import pytest
from httpx import AsyncClient
from src.dependencies.auth import get_current_user_id
from src.main import app
from src.schemas.user import TopUpRequest, PurchaseRequest


@pytest.mark.asyncio
async def test_get_balance(client: AsyncClient, setup_database_with_data):
    user_id = 1

    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    response = await client.get("/api/v1/user/balance")
    assert response.status_code == 200

    data = response.json()
    assert "balance" in data
    assert isinstance(data["balance"], (float, int))

    del app.dependency_overrides[get_current_user_id]


@pytest.mark.asyncio
async def test_top_up_balance(client: AsyncClient, setup_database_with_data):
    user_id = 1
    amount_to_top_up = 50.0

    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    payload = TopUpRequest(amount=amount_to_top_up).dict()
    response = await client.post("/api/v1/user/balance/top-up", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "new_balance" in data

    del app.dependency_overrides[get_current_user_id]


@pytest.mark.asyncio
async def test_purchase_items(client: AsyncClient, setup_database_with_data):
    user_id = 1
    uris_to_purchase = ["uri1", "uri2"]

    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    payload = PurchaseRequest(uris=uris_to_purchase).dict()
    response = await client.post("/api/v1/purchase", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"] == "Purchase successful"

    del app.dependency_overrides[get_current_user_id]


@pytest.mark.asyncio
async def test_purchase_items_insufficient_balance(client: AsyncClient, setup_database_with_data):
    user_id = 1
    uris_to_purchase = ["uri1", "uri2", "uri3"]

    async def override_get_current_user_id():
        return user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    payload = PurchaseRequest(uris=uris_to_purchase).dict()
    response = await client.post("/api/v1/purchase", json=payload)
    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Insufficient balance"

    del app.dependency_overrides[get_current_user_id]
