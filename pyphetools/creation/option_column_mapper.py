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
        # Either have self._option_d be an empty dictionary or it must be a valid dictionary
        if option_d is None:
            self._option_d = {}
        else:
            if not isinstance(option_d, dict):
                raise ValueError(f"option_d argument must be dictionary but was {type(option_d)}")
            self._option_d = option_d
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        chunk = cell_contents.strip()
        results = self._hpo_cr.parse_cell(cell_contents=chunk, custom_d=self._option_d)
        if results is None:
            return []
        else:
            return results
        
    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            column_val = []
            results  = self.map_cell(str(value))
            if results is None:
                print(f"Got None results for {str(value)}")
                dlist.append({"terms": "n/a"})  
            elif len(results) > 0:
                for hpterm in results:
                    column_val.append(f"{hpterm.id} ({hpterm.label}/{hpterm.display_value})")
                dlist.append({"terms": "; ".join(column_val)})  
            else:
                dlist.append({"terms": "n/a"})  
        return pd.DataFrame(dlist)     
   