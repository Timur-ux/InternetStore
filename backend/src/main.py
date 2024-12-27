from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import auth, items, admin, user

# Initialize application
app = FastAPI(
    title="Internet Store API",
    description="API для интернет-магазина",
    version="1.0.0",
    docs_url="/swagger",  # Переопределяет URL Swagger UI
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

app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(items.router, prefix="/api/v1", tags=["Items"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])
app.include_router(user.router, prefix="/api/v1", tags=["UserActions"])

@app.get("/")
def index():
    return {"message": "Welcome to the Internet Store API"}
