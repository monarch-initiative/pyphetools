from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer
from typing import List
import pandas as pd
import re
from collections import defaultdict

class OptionColumnMapper(ColumnMapper):
    
    def __init__(self, concept_recognizer, option_d):
        """Mapper to be used if the column has a set of defined items but text mining is not required.

        Args:
            option_d (dict): key: item (e.g., MVP) in original publication; value: corresponding HPO label, e.g. Mitral Valve Prolapse

        Raises:
            ValueError: if option_d is not a dictionary
        """
        super().__init__()
        # Either have self._option_d be an empty dictionary or it must be a valid dictionary
        if option_d is None or not isinstance(option_d, dict):
            raise ValueError(f"option_d argument must be dictionary but was {type(option_d)}")
        self._option_d = option_d
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer arg must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._hpo_cr = concept_recognizer
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        """Map cell contents using the option dictionary 
        
        Args:
            cell_contents (str): contents of one table cell
        """
        contents = cell_contents.strip()
        delimiters = ',;|/'
        regex_pattern = '|'.join(map(re.escape, delimiters))
        chunks = re.split(regex_pattern, contents)
        chunks = [chunk.strip() for chunk in chunks]
        results = []
        for c in chunks:
            hpo_array = self._option_d.get(c)
            if hpo_array is None:
                continue  # We do not expect to map all items in the column, e.g., negatives or empties are skipped
            if isinstance(hpo_array, list):
                hpo_label = hpo_array[0]
            else:
                hpo_label = hpo_array
            # Note that an Exception will be thrown in HpoExactConceptRecognizer if something goes wrong
            # so that we do not add any additional checks here
            term = self._hpo_cr.get_term_from_label(label=hpo_label)
            results.append(term)
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
   