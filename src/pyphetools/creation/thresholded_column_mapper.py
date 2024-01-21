from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .thresholder import Thresholder
from typing import List
import pandas as pd
import pkg_resources
from collections import defaultdict
import math


class ThresholdedColumnMapper(ColumnMapper):
    INITIALIZED = False

    def __init__(self, column_name, hpo_term_low=None, hpo_term_high=None, hpo_term_abn=None, threshold_low=None, threshold_high=None):
        super().__init__(column_name=column_name)
        self._thresholder = Thresholder(hpo_term_low=hpo_term_low, hpo_term_high=hpo_term_high, hpo_term_abn=hpo_term_abn, threshold_low=threshold_low, threshold_high=threshold_high)
        ThresholdedColumnMapper.init_thresholders_if_needed()

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
        for k, v in mapping_counter.items():
            d = {"mapping": k, "count": str(v)}
            dlist.append(d)
        return pd.DataFrame(dlist)

    @staticmethod
    def init_thresholders_if_needed():
        if ThresholdedColumnMapper.INITIALIZED:
            return
        stream = pkg_resources.resource_stream(__name__, 'data/thresholds.tsv')
        df = pd.read_csv(stream, sep="\t")
        for _, row in df.iterrows():
            print(row)
        ThresholdedColumnMapper.INITIALIZED = True
