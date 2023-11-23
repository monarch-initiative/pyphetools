from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from typing import List, Dict
import pandas as pd
from collections import defaultdict


def get_separate_hpos_from_df(df, hpo_cr):
    """Loop through all the cells in a dataframe or series and try to parse each cell as HPO term.
    Useful when the separate HPO terms are in the cells themselves.

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






class SimpleColumnMapper(ColumnMapper):
    """ColumnMapper for columns that contain information about a single phenotypic abnormality only

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
    def __init__(self, hpo_id, hpo_label, observed=None, excluded=None, non_measured=None):
        """
        Constructor
        """
        super().__init__()
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
        if contents in self._observed:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)]
        elif contents in self._excluded:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)]
        else:
            return [HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, measured=False)]

    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            value = self.map_cell(str(value))
            hpterm = value[0]
            dlist.append({"term": hpterm.hpo_term_and_id, "status": hpterm.display_value})
        return pd.DataFrame(dlist)

class SimpleColumnMapperGenerator:
    """Convenience tool to provide mappings automatically

    Try to map the columns in a dataframe by matching the name of the column to correct HPO term.
    This class can be used to generate SimpleColumn mappers for exact matches found in the columns names.

    :param df: dataframe with phenotypic data
    :type df: pd.DataFrame
    :param observed: symbol used in table if the phenotypic feature was observed
    :type observed: str
    :param excluded: symbol used if the feature was excluded
    :type excluded: str
    :param hpo_cr: instance of HpoConceptRecognizer to match HPO term and get label/id
    :type hpo_cr: HpoConceptRecognizer
    """
    def __init__(self, df, observed, excluded, hpo_cr) -> None:
        """
        Constructor
        """
        self._df = df
        self._observed = observed
        self._excluded = excluded
        self._hpo_cr = hpo_cr
        self._mapped_columns = []
        self._unmapped_columns = []
        self._error_messages = []


    def try_mapping_columns(self) -> Dict[str, ColumnMapper]:
        """As a side effect, this class initializes three lists of mapped, unmapped, and error columns

        :returns: A dictionary with successfully mapped columns
        :rtype: Dict[str,ColumnMapper]
        """
        simple_mappers = defaultdict(ColumnMapper)
        for col in self._df.columns:
            colname = str(col)
            if self._hpo_cr.contains_term_label(colname):
                hpo_term_list = self._hpo_cr.parse_cell(colname)
                hpo_term = hpo_term_list[0]
                simple_mappers[col] = SimpleColumnMapper(hpo_id=hpo_term.id,
                                                                    hpo_label=hpo_term.label,
                                                                    observed=self._observed,
                                                                    excluded=self._excluded)
            else:
                self._unmapped_columns.append(colname)
        self._mapped_columns = list(simple_mappers.keys())
        return simple_mappers


    def get_unmapped_columns(self):
        """
        :returns: A list of names of the columns that could not be mapped
        :rtype: List[str]
        """
        return self._unmapped_columns

    def get_mapped_columns(self) -> List[str]:
        """
        :returns: A list of names of the columns that were mapped
        :rtype: List[str]
        """
        return self._mapped_columns

    def to_html(self):
        """create an HTML table with names of mapped and unmapped columns
        """
        table_items = []
        table_items.append('<table style="border: 2px solid black;">\n')
        table_items.append("""<tr>
            <th>Result</th>
            <th>Columns</th>
        </tr>
      """)
        mapped_str = "; ".join(self._mapped_columns)
        unmapped_str = "; ".join([f"<q>{colname}</q>" for colname in self._unmapped_columns])
        def two_item_table_row(cell1, cell2):
            return f"<tr><td>{cell1}</td><td>{cell2}</td></tr>"
        table_items.append(two_item_table_row("Mapped", mapped_str))
        table_items.append(two_item_table_row("Unmapped", unmapped_str))
        table_items.append('</table>\n') # close table content
        return "\n".join(table_items)
