from __future__ import annotations

from query_builder import QueryBuilder


class Update(QueryBuilder):
    def __init__(self, table_name) -> None:
        super().__init__()
        self._query.append(f'UPDATE {table_name}')

    def set(self, field, value) -> Update:
        self._query.append(f'SET {field} = {value}')
        return self

    def where(self, value) -> Update:
        self._query.append(f'WHERE {value}')
        return self

    def equal(self, value) -> Update:
        self._query.append(f'= {value}')
        return self

    def notequal(self, value) -> Update:
        self._query.append(f'= {value}')
        return self

    def less(self, value) -> Update:
        self._query.append(f'< {value}')
        return self

    def greater(self, value) -> Update:
        self._query.append(f'> {value}')
        return self
