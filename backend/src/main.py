from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import auth, items, admin
from src.core.config import DB_CONFIG
from src.db.sessionManager import SessionManager

# Initialize application
app = FastAPI(
    title="Internet Store API",
    version="1.0.0",
)

# CORS settings
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)

# Initialize session manager
sessionManager = SessionManager(DB_CONFIG)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(items.router, prefix="/api/v1", tags=["Items"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])

@app.get("/")
def index():
    return {"message": "Welcome to the Internet Store API"}
