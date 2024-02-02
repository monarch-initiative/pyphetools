from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .thresholder import Thresholder
from typing import List
import pandas as pd
import pkg_resources
from collections import defaultdict
import math


class ThresholdedColumnMapper(ColumnMapper):

    def __init__(self, column_name, thresholder:Thresholder):
        super().__init__(column_name=column_name)
        self._thresholder = thresholder

    def map_cell(self, cell_contents) -> List[HpTerm]:
        hpterm = self._thresholder.map_value(cell_contents=cell_contents)
        if hpterm is not None:
            return [hpterm]
        else:
            return []


    def preview_column(self, df:pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be pandas DataFrame, but was {type(column)}")
        column = df[self._column_name]
        mapping_counter = defaultdict(int)
        for _, value in column.items():
            results = self.map_cell(str(value))
            if len(results) > 0:
                hpterm = results[0]
                mapped = f"{hpterm.hpo_term_and_id}: {hpterm.display_value}"
                mapping_counter[mapped] += 1
        dlist = []
        colname = f"mapping: {self._thresholder.get_reference_range()}"
        for k, v in mapping_counter.items():
            d = {colname: k, "count": str(v)}
            dlist.append(d)
        return pd.DataFrame(dlist)

