from pydantic import BaseModel
from typing import List, Optional


class BalanceResponse(BaseModel):
    balance: float


class TopUpRequest(BaseModel):
    amount: float


class TopUpResponse(BaseModel):
    new_balance: float


class PurchaseRequest(BaseModel):
    uris: List[str]


class PurchaseResponse(BaseModel):
    message: str
