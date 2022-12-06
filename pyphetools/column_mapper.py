from collections import defaultdict
from typing import List


class ColumnMapper:
    def __init__(self, custom_map_d) -> None:
        if custom_map_d is None:
            self._custom_map_d = defaultdict()
        else:
            self._custom_map_d = custom_map_d


    def map_cell(self, cell_contents) -> List:
        return []