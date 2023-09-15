from collections import defaultdict
from typing import List
import pandas as pd
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer


class CustomColumnMapper(ColumnMapper):
    def __init__(self, concept_recognizer, custom_map_d=None, excluded_set=None) -> None:
        """Column mapper for concept recognition (CR) augmented by custom maps for concepts missed by automatic CR

        Args:
            concept_recognizer (HpoConceptRecognizer):  Concept Recognition object.
            custom_map_d (dict): keys -- label of a concept in the original text; values -- corresponding HPO label
            excluded_set (set): set of strings to be excluded from concept recognition
        """
        super().__init__()
        if custom_map_d is None:
            self._custom_map_d = defaultdict()
        else:
            self._custom_map_d = custom_map_d
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer arg must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._concept_recognizer = concept_recognizer
        if excluded_set is None:
            excluded_set = set()
        self._excluded_set = excluded_set

    def map_cell(self, cell_contents) -> List:
        """Perform concept recognition on one cell of the table

        Args:
            cell_contents (str): text to be used for concept recognition.

        This method should not be used by client code. Instead, it is called
        by the CohortEncoder object, which should provide the id_to_primary_d, label_to_id_d
        objects representing the automatic HPO dictionaries. It is designed to take
        the contents of a single cell in a Supplemental Table and to parse out 
        HPO terms.
        For now, we use a naive implementation that searches for exact matches. Moving forward
        it should be possible to implement the algorithm of fenominal that removes stop words
        and searches for ontology concepts in which the remaining tokens occur in any order.
        """
        for excl in self._excluded_set:
            cell_contents = cell_contents.replace(excl, " ")
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
            preview_d[value] = self.map_cell(str(value))
        dlist = []
        for k, v in preview_d.items():
            if v is None or len(v) == 0:
                terms = "n/a"
            else:
                terms = "; ".join([hpo.to_string() for hpo in v])
            dlist.append({"column": k, "terms": terms})
        return pd.DataFrame(dlist)
