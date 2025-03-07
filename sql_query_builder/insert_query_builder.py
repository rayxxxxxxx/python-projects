from __future__ import annotations

from query_builder import QueryBuilder


class Insert(QueryBuilder):
    def __init__(self, table_name) -> None:
        super().__init__()
        self._query.append(f'INSERT INTO {table_name}')

    def fields(self, fields: list) -> Insert:
        fields_str = f'({", ".join(fields)})'
        self._query.append(fields_str)
        return self

    def value(self, row: list) -> Insert:
        row_str = ", ".join(row)
        self._query.append(f'VALUES {row_str}')
        return self

    def values(self, rows: list) -> Insert:
        rows_str = ", ".join([f'({", ".join(r)})' for r in rows])
        self._query.append(f'VALUES {rows_str}')
        return self
