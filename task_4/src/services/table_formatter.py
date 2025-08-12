from typing import List

from src.setup_logger import decorate_all_methods


@decorate_all_methods
class TableFormatter:
    def __init__(self, headers: List[str], rows: List[List[str]]):
        self.headers = headers
        self.rows = rows
        self.all_rows = [headers] + rows
        self.col_widths = self._calc_col_widths()

    def _calc_col_widths(self) -> List[int]:
        col_widths = [
            max(len(row[i]) for row in self.all_rows)
            for i in range(len(self.headers))
        ]
        return col_widths

    async def format_row(self, row: List[str]) -> str:
        formatted_row = " | ".join(f"{cell:<{self.col_widths[i]}}" for i, cell in enumerate(row))
        return formatted_row

    async def print_table(self) -> None:
        print()
        header = await self.format_row(self.headers)
        print(header)
        print("-+-".join("-" * w for w in self.col_widths))
        for row in self.rows:
            line = await self.format_row(row)
            print(line)

    def __repr__(self):
        return (f"<TableFormatter(headers={self.headers!r}, "
                f"rows_count={len(self.rows)}, "
                f"col_widths={self.col_widths})>")
