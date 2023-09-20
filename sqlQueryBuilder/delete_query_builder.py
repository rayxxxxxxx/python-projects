from __future__ import annotations

from query_builder import QueryBuilder


class Delete(QueryBuilder):
    def __init__(self, table_name) -> None:
        super().__init__()
        self._query.append(f'DELETE FROM {table_name}')

    def where(self, value) -> Delete:
        self._query.append(f'WHERE {value}')
        return self

    def equal(self, value) -> Delete:
        self._query.append(f'= {value}')
        return self

    def notequal(self, value) -> Delete:
        self._query.append(f'= {value}')
        return self

    def less(self, value) -> Delete:
        self._query.append(f'< {value}')
        return self

    def greater(self, value) -> Delete:
        self._query.append(f'> {value}')
        return self
