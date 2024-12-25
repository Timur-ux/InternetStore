from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.db.sessionManager as sm
from src.core.config import DB_CONFIG
import json


sessionManager = sm.SessionManager(DB_CONFIG)

app = FastAPI()

# origins = [
#         "*"
#         ]
#
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_headers=['*'],
#         allow_methods=['*'],
#         )

@app.get("/")
def forecast(items: Optional[List[int]] = None):
    """Do forecast for `items` if given else for all existing items"""
    pass

