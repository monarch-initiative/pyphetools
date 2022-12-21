from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from typing import List
import pandas as pd

class SimpleColumnMapper(ColumnMapper):
    
    def __init__(self, hpo_id, hpo_label, observed=None, excluded=None, non_measured = None, constant=False):
        """_summary_

        Args:
            hpo_id (_type_): _description_
            hpo_label (_type_): _description_
            observed (_type_): _description_
            excluded (_type_): _description_
            non_measured (_type_, optional): _description_. Defaults to None.
            constant (bool, optional): If true, all patients have this feature. Defaults to False.
        """
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        if observed is None or excluded is None:
            if not constant:
                raise ValueError("constant argument must be true if not arguments are provided for observed and excluded")
        if constant:
            self._observed = set()
            self._excluded = set()
        else:
            self._observed = set(observed)
            self._excluded = set(excluded)
        self._not_measured = non_measured
        self._constant = constant
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        if self._constant:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label)]
        if not isinstance(cell_contents, str):
            raise ValueError(f"Error: cell_contents argument ({cell_contents}) must be string but was {type(cell_contents)} -- coerced to string")
        contents = cell_contents.strip()
        if contents in self._observed:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label)]
        elif contents in self._excluded:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label, observed=False)]
        else:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label, measured=False)]


    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            value  = self.map_cell(str(value))
            hpterm = value[0]
            dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)  
    
        
        
    

