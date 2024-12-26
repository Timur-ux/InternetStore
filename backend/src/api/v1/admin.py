from fastapi import APIRouter, HTTPException
from src.services.admin import get_sales_forecast
from src.dependencies.auth import get_user_type
from src.models.forecast import ForecastRequest
from src.models.user import User

router = APIRouter()

@router.post("/admin/forecast")
async def get_forecast(
    forecast_request: ForecastRequest,
    user_type: str = Depends(get_user_type)
):
    # Проверим, является ли пользователь администратором
    if user_type != 'Администратор':
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Получаем прогноз
    forecast_data = await get_sales_forecast(
        item_ids=forecast_request.item_ids,
        item_uris=forecast_request.item_uris
    )
    
    return {"forecast": forecast_data}