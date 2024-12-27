from fastapi import APIRouter, HTTPException, Depends
from src.services.admin import get_sales_forecast
from src.dependencies.auth import get_user_type
from src.schemas.admin import ForecastRequest, ForecastResponse

router = APIRouter()

@router.post(
    "/admin/forecast",
    summary="Получить прогноз продаж",
    response_model=ForecastResponse,
)
async def get_forecast(
    request: ForecastRequest,
    user_type: str = Depends(get_user_type),
):
    # Проверим, является ли пользователь администратором
    if user_type != "Администратор":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Получаем прогноз
    forecast_data = await get_sales_forecast(item_uris=request.uris)
    return {"forecast": forecast_data}
