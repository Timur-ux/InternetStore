from pydantic import BaseModel
from typing import List, Optional


class ItemResponse(BaseModel):
    id: int
    name: str
    uri: str
    price: Optional[float]

    class Config:
        orm_mode = True


class ItemsListResponse(BaseModel):
    items: List[ItemResponse]


class ItemsByUriRequest(BaseModel):
    uris: List[str]
