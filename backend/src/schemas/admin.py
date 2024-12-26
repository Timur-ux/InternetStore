from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ForecastRequest(BaseModel):
    uris: Optional[List[str]] = None


class ForecastResponse(BaseModel):
    forecast: List[Dict[str, Any]]  # Каждый объект в списке содержит данные прогноза
