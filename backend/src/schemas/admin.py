from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ForecastRequest(BaseModel):
    uris: List[str]


class ForecastResponse(BaseModel):
    forecast: Any  # Каждый объект в списке содержит данные прогноза
