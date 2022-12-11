from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer
from typing import List
import pandas as pd
from collections import defaultdict

class OptionColumnMapper(ColumnMapper):
    
    def __init__(self, concept_recognizer, option_d):
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._hpo_cr = concept_recognizer
        if not isinstance(option_d, dict):
            raise ValueError(f"option_d argument must be dictionary but was {type(option_d)}")
        self._option_d = option_d
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        chunk = cell_contents.strip()
        if chunk in self._option_d:
            hpo_label = self._option_d.get(chunk)
            return self._hpo_cr.parse_cell(hpo_label)
        else:
            return []

    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            results  = self.map_cell(str(value))
            if len(results) > 0:
                hpterm = results[0]
                dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)     
   