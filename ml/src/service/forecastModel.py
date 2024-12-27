import catboost
from catboost import Pool
from catboost import CatBoostRegressor
import pandas as pd
from typing import List


class ForecastModel:
    def __init__(self, modelName: str, preparedDataPath: str):
        self.modelName = modelName
        self.model = CatBoostRegressor()
        self.model.load_model(modelName)

    def predict(self, items: List[int]):
        """not realized yet"""
        pass
