from numpy.random import rand
from typing import List

class RandomModel:
    def predict(self, item_ids: List[str]):
        return list(map(lambda x: 100*rand(), item_ids))
