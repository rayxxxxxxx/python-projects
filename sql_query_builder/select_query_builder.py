from __future__ import annotations

from query_builder import QueryBuilder


class Select(QueryBuilder):
    def __init__(self, fields: list) -> None:
        super().__init__()
        self._query.append(f'SELECT {", ".join(fields)}')

    def from_(self, table_name) -> Select:
        self._query.append(f'FROM {table_name}')
        return self

    def into(self, table_name) -> Select:
        self._query.append(f'INTO {table_name}')
        return self

    def ijoin(self, table_name) -> Select:
        self._query.append(f'INNER JOIN {table_name}')
        return self

    def ljoin(self, table_name) -> Select:
        self._query.append(f'LEFT JOIN {table_name}')
        return self

    def rjoin(self, table_name) -> Select:
        self._query.append(f'RIGHT JOIN {table_name}')
        return self

    def on(self, field1, field2) -> Select:
        self._query.append(f'ON {field1} = {field2}')
        return self

    def where(self, value) -> Select:
        self._query.append(f'WHERE {value}')
        return self

    def equal(self, value) -> Select:
        self._query.append(f'= {value}')
        return self

    def notequal(self, value) -> Select:
        self._query.append(f'= {value}')
        return self

    def less(self, value) -> Select:
        self._query.append(f'< {value}')
        return self

    def greater(self, value) -> Select:
        self._query.append(f'> {value}')
        return self
