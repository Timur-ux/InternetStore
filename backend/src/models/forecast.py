from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ForecastRequest(BaseModel):
    item_uris: Optional[List[str]] = None  # Список URI товаров

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
