from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from typing import List
import pandas as pd
from collections import defaultdict


def get_separate_hpos_from_df(df, hpo_cr):
    """Loop through all the cells in a dataframe or series and try to parse each cell as HPO term.
    Useful when the seperate HPO terms are in the cells themselves.

      Args:
         df (dataframe): dataframe with phenotypic data
         hpo_cr (HpoConceptRecognizer): instance of HpoConceptRecognizer to match HPO term and get label/id

      Returns:
          additional_hpos: list of lists with the additional HPO terms per individual
      """
    additional_hpos = []

    for i in range(len(df)):
        temp_hpos = []
        for y in range(df.shape[1]):
            hpo_term = hpo_cr.parse_cell(df.iloc[i, y])
            if len(hpo_term) > 0:
                temp_hpos.extend(hpo_term)
        additional_hpos.append(list(set(temp_hpos)))
    return additional_hpos


def try_mapping_columns(df, observed, excluded, hpo_cr, preview=True):
    """Try to map the columns in a dataframe by matching the name of the column to correct HPO term.
    Wrapper for SimpleColumnMapper below

    Args:
       df (dataframe): dataframe with phenotypic data
       observed (str): symbol used in table if the phenotypic feature was observed
       excluded (str): symbol used if the feature was excluded
       hpo_cr (HpoConceptRecognizer): instance of HpoConceptRecognizer to match HPO term and get label/id
       preview (bool): whether to print the successfully mapped columns

    Returns:
        simple_mappers (dict): dict with successfully mapped columns
        col_not_found (list): columns that were not mapped
    """
    col_not_found = []
    simple_mappers = defaultdict(ColumnMapper)
    for col in df.columns:
        hpo_term = hpo_cr.parse_cell(col)
        if len(hpo_term) > 0:
            hpo_term = hpo_term[0]
            simple_mappers[col] = SimpleColumnMapper(hpo_id=hpo_term.id,
                                                                hpo_label=hpo_term.label,
                                                                observed=observed,
                                                                excluded=excluded)
            if preview:
                print(simple_mappers[col].preview_column(df[col]))
        else:
            col_not_found.append(col)
    return simple_mappers, col_not_found


class SimpleColumnMapper(ColumnMapper):

    def __init__(self, hpo_id, hpo_label, observed=None, excluded=None, non_measured=None, constant=False):
        """_summary_

        Args:
            hpo_id (_type_): HPO  id, e.g., HP:0004321
            hpo_label (_type_): Corresponding term label
            observed (_type_): symbol used in table if the phenotypic feature was observed
            excluded (_type_): symbol used if the feature was excluded
            non_measured (_type_, optional): symbol used if the feature was not measured or is N/A. Defaults to None.
            constant (bool, optional): If true, all patients have this feature. Defaults to False.
        """
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        if observed is None or excluded is None:
            if not constant:
                raise ValueError(
                    "constant argument must be true if not arguments are provided for observed and excluded")
        if constant:
            self._observed = set()
            self._excluded = set()
        else:
            self._observed = observed
            self._excluded = excluded
        self._not_measured = non_measured
        self._constant = constant

    def map_cell(self, cell_contents) -> List[HpTerm]:
        if self._constant:
            return [HpTerm(id=self._hpo_id, label=self._hpo_label)]
        if not isinstance(cell_contents, str):
            raise ValueError(
                f"Error: cell_contents argument ({cell_contents}) must be string but was {type(cell_contents)} -- coerced to string")
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
            value = self.map_cell(str(value))
            hpterm = value[0]
            dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)
