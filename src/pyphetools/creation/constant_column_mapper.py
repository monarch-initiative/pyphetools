from typing import List
import pandas as pd
from collections import defaultdict
from .column_mapper import ColumnMapper
from .hp_term import HpTerm


class ConstantColumnMapper(ColumnMapper):
    """Column mapper for cases in which all patients have an (optionally excluded) HPO term.
    :param column_name: name of the column in the pandas DataFrame
    :type column_name: str
    :param hpo_id: HPO  id, e.g., HP:0004321
    :type hpo_id: str
    :param hpo_label: Corresponding term label
    :type hpo_label: str
    :param term_list: list of lists with [label, hpo_id
    :type term_list: List[lst]
    :param excluded: if True, then all individuals had this feature explicitly excluded
    :type excluded: bool
    """
    def __init__(self, column_name,  hpo_id=None, hpo_label=None, term_list=None, excluded:bool=False) -> None:

        super().__init__(column_name=column_name)
        self._hpo_id = hpo_id
        if hpo_id is None and hpo_label is None and term_list is not None:
            self._hpo_terms = []
            for term in term_list:
                if excluded:
                    hpoterm = HpTerm(label=term[0], hpo_id=term[1], observed=False)
                else:
                    hpoterm = HpTerm(label=term[0], hpo_id=term[1], observed=True)
                self._hpo_terms.append(hpoterm)
        elif term_list is None and hpo_id is not None and hpo_label is not None:
            if excluded:
                hpoterm = HpTerm(label=hpo_label, hpo_id=hpo_id, observed=False)
            else:
                hpoterm = HpTerm(label=hpo_label, hpo_id=hpo_id, observed=True)
            self._hpo_terms = [hpoterm]
        else:
            raise ValueError(f"Error: Either hpo_id and hpo_label are not not or a list of HPO terms is passed")
        self._excluded = excluded

    def map_cell(self, cell_contents) -> List[HpTerm]:
        """if this mapper is used, then all individuals in the table have the list of HPO terms

        Args:
            cell_contents (str): not used, can be None or any other value

        Returns:
            List[HpTerm]: list of HPO terms
        """
        return self._hpo_terms

    def preview_column(self, df:pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be pandas DataFrame, but was {type(column)}")
        mapping_counter = defaultdict(int)

        dlist = []
        column = df[self._column_name]
        for _, value in column.items():
            display = ";".join(hpterm.display_value for hpterm in self._hpo_terms)
            display = f"{value} -> {display}"
            mapping_counter[display] +=1
        for k, v in mapping_counter.items():
            d = {"mapping": k, "count": str(v)}
            dlist.append(d)
        return pd.DataFrame(dlist)

