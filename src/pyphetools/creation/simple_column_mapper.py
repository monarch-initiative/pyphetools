from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .pyphetools_age import IsoAge
from typing import List
import pandas as pd
import re
from collections import defaultdict


def get_separate_hpos_from_df(df, hpo_cr):
    """Loop through all the cells in a dataframe or series and try to parse each cell as HPO term.
    Useful when the separate HPO terms are in the cells themselves.

    :param df: dataframe with phenotypic data
    :type df: pd.DataFrame
    :param hpo_cr: instance of HpoConceptRecognizer to match HPO term and get label/id
    :type hpo_cr: HpoConceptRecognizer
    :returns: list of lists with the additional HPO terms per individual
    :rtype: List[List[HpTerm]]
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


class SimpleColumnMapper(ColumnMapper):
    """ColumnMapper for columns that contain information about a single phenotypic abnormality only
    :param column_name: name of the column in the pandas DataFrame
    :type column_name: str
    :param hpo_id: HPO  id, e.g., HP:0004321
    :type hpo_id: str
    :param hpo_label: Corresponding term label
    :type hpo_label: str
    :param observed: symbol used in table if the phenotypic feature was observed
    :type observed: str
    :param excluded: symbol used if the feature was excluded
    :type excluded: str
    :param non_measured: symbol used if the feature was not measured or is N/A. Defaults to None, optional
    :type non_measured: str
    """
    def __init__(self, column_name, hpo_id, hpo_label, observed=None, excluded=None, non_measured=None):
        """
        Constructor
        """
        super().__init__(column_name=column_name)
        self._hpo_id = hpo_id
        self._hpo_label = hpo_label
        if observed is None or excluded is None:
            raise ValueError(
                    "Need to provide arguments for both observed and excluded")
        self._observed = observed
        self._excluded = excluded
        self._not_measured = non_measured

    def map_cell(self, cell_contents) -> List[HpTerm]:
        if not isinstance(cell_contents, str):
            raise ValueError(
                f"Error: cell_contents argument ({cell_contents}) must be string but was {type(cell_contents)} -- coerced to string")
        contents = cell_contents.strip()
        # first check if the cell contents represent a valid iso8601, which represents age of onset.
        if ColumnMapper.is_valid_iso8601(contents):
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, onset=IsoAge(contents))]
        if contents in self._observed:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)]
        elif contents in self._excluded:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
        else:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, measured=False)]

    def preview_column(self, df:pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be pandas DataFrame, but was {type(column)}")
        column = df[self._column_name]
        mapping_counter = defaultdict(int)
        for _, value in column.items():
            cell_contents = str(value)
            value = self.map_cell(cell_contents)
            hpterm = value[0]
            mapped = f"original value: \"{cell_contents}\" -> HP: {hpterm.hpo_term_and_id} ({hpterm.display_value})"
            mapping_counter[mapped] += 1
        dlist = []
        for k, v in mapping_counter.items():
            d = {"mapping": k, "count": str(v)}
            dlist.append(d)
        return pd.DataFrame(dlist)
