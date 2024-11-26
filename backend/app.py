#!venv/bin/python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.db.sessionManager as sm
from src.db.requests import processAuth
from src.core.config import DB_CONFIG
import json


sessionManager = sm.SessionManager(DB_CONFIG)

app = FastAPI()

origins = [
        "http://localhost:8080"
        ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_headers=['*'],
        allow_methods=['*'],
        )

@app.get("/")
def index():
    response = {"data": "Hello world"}
    return json.dumps(response)

@app.get('/api/login')
def auth():
    # Do some auth login
    return "some auth data"

@app.get('/api/products')
def getProductList():
    # Do some get product list logic
    return "product list"
