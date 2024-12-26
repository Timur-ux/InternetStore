from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    login: str
    password: str


class RegisterResponse(BaseModel):
    message: str
    user_id: int


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    message: str
    token: str
    user_type: str
