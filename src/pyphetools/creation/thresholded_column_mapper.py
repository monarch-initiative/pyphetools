from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from typing import List
import pandas as pd
import math


class ThresholdedColumnMapper(ColumnMapper):
    def __init__(self, hpo_id, hpo_label, threshold, call_if_above, observed_code=None):
        super().__init__()
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        if not isinstance(threshold, int) and not isinstance(threshold, float):
            raise ValueError(f"threshold argument must be integer or float but was {threshold}")
        if not isinstance(call_if_above, bool):
            raise ValueError(f"call_if_above argument must be True or False but was {call_if_above}")
        self._threshold = float(threshold)  # transform ints to float for simplicity, it will not affect result
        self._call_if_above = call_if_above
        self._observed_code = observed_code

    def map_cell(self, cell_contents) -> List[HpTerm]:
        if isinstance(cell_contents, str):
            contents = cell_contents.strip()
            if contents == self._observed_code:
                return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)]
            if contents.lower() == "nan":
                return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
        elif isinstance(cell_contents, int):
            contents = cell_contents
        elif isinstance(cell_contents, float):
            if math.isnan(cell_contents):
                return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
            contents = cell_contents
        else:
            raise ValueError(
                f"Malformed cell contents for ThresholdedColumnMapper: {cell_contents}, type={type(cell_contents)}")
        try:
            
            value = float(contents)
            if self._call_if_above:
                if value > self._threshold:
                    return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)]
                else:
                    return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
            else:
                if value > self._threshold:
                    return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
                else:
                    return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)]
        except Exception as exc:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, measured=False)]

    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            results = self.map_cell(str(value))
            if len(results) > 0:
                hpterm = results[0]
                dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)
