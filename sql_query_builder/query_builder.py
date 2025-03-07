from __future__ import annotations
from abc import ABC


class QueryBuilder(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._query = []

    def build(self):
        return ' '.join(self._query)+';'
