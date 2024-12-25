from fastapi import APIRouter, Depends, HTTPException, Header
from src.db.requests import verify_jwt, create_user, authenticate_user
from src.models import LoginModel, RegModel
from src.db.sessionManager import SessionManager

router = APIRouter()

@router.post("/register")
def register(user: RegModel, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    token = authorization.split(" ")[1]
    if user.access_level == 2:
        try:
            decoded_token = verify_jwt(token)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
    try:
        create_user(SessionManager, user.login, user.password, user.access_level)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

@router.post("/login")
def login(user: LoginModel):
    token = authenticate_user(SessionManager, user.login, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {"token": token}
