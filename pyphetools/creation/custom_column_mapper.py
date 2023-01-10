from collections import defaultdict
from typing import List
import pandas as pd
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer


class CustomColumnMapper(ColumnMapper):
    def __init__(self, concept_recognizer, custom_map_d=None) -> None:
        if custom_map_d is None:
            self._custom_map_d = defaultdict()
        else:
            self._custom_map_d = custom_map_d
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._concept_recognizer = concept_recognizer


    def map_cell(self, cell_contents) -> List:
        """
        This method should not be used by client code. Instead, it is called
        by the CohortEncoder object, which should provide the id_to_primary_d, label_to_id_d
        objects representing the automatic HPO dictionaries. It is designed to take
        the contents of a single cell in a Supplemental Table and to parse out 
        HPO terms.
        For now, we use a naive implementation that searches for exact matches. Moving forward
        it should be possible to implement the algorithm of fenominal that removes stop words
        and searches for ontology concepts in which the remaining tokens occur in any order.
        """
        results = self._concept_recognizer.parse_cell(cell_contents=cell_contents, custom_d=self._custom_map_d)
        if results is None:
            return []
        else:
            return results


    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        preview_d = defaultdict(list)
        for index, value in column.items():
            preview_d[value]  = self.map_cell(str(value))
        dlist = []
        for k, v in preview_d.items():
            if v is None or len(v) == 0:
                terms = "n/a"
            else:
                terms = "; ".join([hpo.to_string() for hpo in v])
            dlist.append({"column": k, "terms": terms})
        return pd.DataFrame(dlist)
    
   
            
        