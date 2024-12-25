from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from services.auth_service import verify_jwt, create_user, authenticate_user
from models.user import RegModel, LoginModel
from db.init import get_db

router = APIRouter()

@router.post("/register")
def register(user: RegModel, authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    token = authorization.split(" ")[1]
    if user.access_level == 2:
        try:
            decoded_token = verify_jwt(token)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
    try:
        create_user(db, user.login, user.password, user.access_level)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

@router.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db)):
    token = authenticate_user(db, user.login, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {"token": token}