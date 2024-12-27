from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.service.randomModel import RandomModel

app = FastAPI(docs_url="/swagger")

origins = [
        "*"
        ]
#
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_headers=['*'],
        allow_methods=['*'],
        )

model = RandomModel()


class ForecastItems(BaseModel):
    item_uris: List[str]


@app.post("/")
def forecast(items: ForecastItems):
    result = model.predict(items.item_uris)
    response = []
    for k, v in zip(items.item_uris, result):
        response.append({"uri": k, "forecast": v})
    return {"forecast": response}
