from typing import List
import pandas as pd
from .column_mapper import ColumnMapper
from .hp_term import HpTerm

class ConstantColumnMapper(ColumnMapper):
    def __init__(self, hpo_id, hpo_label, excluded=False) -> None:
        """Column mapper for cases in which we known that all patients in the cohort either have an HPO feature or the feature was excluded in all patients.

        Args:
            hpo_id (_type_): HPO  id, e.g., HP:0004321
            hpo_label (_type_): Corresponding term label
            excluded (_type_): symbol used if the feature was excluded
        """
        super().__init__()
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        self._excluded = excluded
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        if self._excluded:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
        else:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=True)]
        
    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        if self._excluded:
            hpterm = HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)
        else:
            hpterm = HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=True)
        for _, value in column.items():
            dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)