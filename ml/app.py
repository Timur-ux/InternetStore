from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.service.randomModel import RandomModel
import src.db.sessionManager as sm
from src.core.config import DB_CONFIG


# sessionManager = sm.SessionManager(DB_CONFIG)

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

model = RandomModel()


class ForecastItems(BaseModel):
    items: List[int]


@app.get("/")
def forecast(items: ForecastItems):
    result = model.predict(items.items)
    return {"predicted_item_cnt_monthly": result}
