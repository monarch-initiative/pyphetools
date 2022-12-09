from collections import defaultdict
from typing import List
import pandas as pd


class ColumnMapper:
    def __init__(self, custom_map_d, id_to_primary_d, label_to_id_d) -> None:
        if custom_map_d is None:
            self._custom_map_d = defaultdict()
        else:
            self._custom_map_d = custom_map_d
        self._id_to_primary_d = id_to_primary_d
        self._label_to_id_d = label_to_id_d


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
        positive_term_id_hits = []
        for k, v in self._custom_map_d.items():
            if k in cell_contents:
                positive_term_id_hits.append(v)

        return positive_term_id_hits


    def preview(column):
        if not isinstance(column, pd.core.series.Series):
            raise ValueError("column argument needs to be pandas Series")
        for _, val in column.iteritems():
            pass