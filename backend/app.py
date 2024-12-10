from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import src.db.requests as db_requests
from src.db.sessionManager import SessionManager
from src.core.config import DB_CONFIG
import json

sessionManager = SessionManager(DB_CONFIG)
app = FastAPI()

# CORS settings
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        return db_requests.verify_jwt(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# Models
class LoginModel(BaseModel):
    login: str
    password: str

class RegModel(BaseModel):
    login: str
    password: str
    access_level: int

class Mark(BaseModel):
    mark_id: int
    mark_type: int
    location_id: int
    last_position: List[float]

@app.get("/")
def index():
    return {"message": "Welcome to the Internet Store API"}

@app.post("/api/register")
def register(user: RegModel):
    try:
        db_requests.create_user(sessionManager, user.login, user.password, user.access_level)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

@app.post("/api/login")
def login(user: LoginModel):
    token = db_requests.authenticate_user(sessionManager, user.login, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {"token": token}

@app.get("/api/marks", dependencies=[Depends(authenticate_user)])
def list_marks():
    return {"marks": db_requests.get_marks(sessionManager)}

@app.get("/api/marks/{mark_id}", dependencies=[Depends(authenticate_user)])
def get_mark(mark_id: int):
    mark = db_requests.get_mark_by_id(sessionManager, mark_id)
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    return mark

@app.put("/api/marks/{mark_id}", dependencies=[Depends(authenticate_user)])
def create_mark(mark_id: int, mark: Mark):
    try:
        db_requests.add_mark(sessionManager, mark.mark_id, mark.mark_type, mark.location_id, mark.last_position)
        return {"message": "Mark created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating mark: {e}")

@app.post("/api/marks/{mark_id}", dependencies=[Depends(authenticate_user)])
def modify_mark(mark_id: int, mark: Mark):
    try:
        db_requests.update_mark(sessionManager, mark_id, mark.mark_type, mark.location_id, mark.last_position)
        return {"message": "Mark updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating mark: {e}")

@app.delete("/api/marks/{mark_id}", dependencies=[Depends(authenticate_user)])
def remove_mark(mark_id: int):
    db_requests.delete_mark(sessionManager, mark_id)
    return {"message": "Mark deleted successfully"}
