from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from typing import List
import pandas as pd
from collections import defaultdict

class SimpleColumnMapper(ColumnMapper):
    
    def __init__(self, hpo_id, hpo_label, observed, excluded, non_measured = None):
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        self._observed = observed
        self._excluded = excluded
        self._not_measured = non_measured
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        if not isinstance(cell_contents, str):
            raise ValueError(f"cell_contents must have string datatype but was {type(cell_contents)}")
        if cell_contents == self._observed:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label)]
        elif cell_contents.trim() == self._excluded:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label, observed=False)]
        else:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label, measured=False)]


    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            value  = self.map_cell(str(value))
            hpterm = value[0]
            dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)  
    
        
        
    

