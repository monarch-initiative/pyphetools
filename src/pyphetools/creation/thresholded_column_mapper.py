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
        ThresholdedColumnMapper.init_thresholders()

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
    def init_thresholders():

        stream = pkg_resources.resource_stream(__name__, 'data/thresholds.tsv')
        df = pd.read_csv(stream, sep="\t")
        thresholders = {}
        for _, row in df.iterrows():
            # label	hpo_abn_label	hpo_abn_id	hpo_low_label	hpo_low_id	hpo_high_label	hpo_high_id	unit	low	high	Reference
            label = row["label"]
            hpo_abn_label = row["hpo_abn_label"]
            hpo_abn_id = row["hpo_abn_id"]
            abn_hp = HpTerm(hpo_id=hpo_abn_id, label=hpo_abn_label)
            hpo_low_label = row["hpo_low_label"]
            hpo_low_id = row["hpo_low_id"]
            low_hp = HpTerm(hpo_id=hpo_low_id, label=hpo_low_label)
            hpo_high_label = row["hpo_high_label"]
            hpo_high_id = row["hpo_high_id"]
            high_hp = HpTerm(hpo_id=hpo_high_id, label=hpo_high_label)
            low = row["low"]
            high = row["high"]
            unit = row["unit"]
            thresholders[label] = Thresholder(hpo_term_abn=abn_hp,
                                            hpo_term_low=low_hp,
                                            hpo_term_high=high_hp,
                                            threshold_low=low,
                                            threshold_high=high,
                                            unit=unit)
        Thresholder.ALKALINE_PHOSPHATASE = thresholders.get("alkaline phosphatase concentration")
        # etc. with other items from the file ?

