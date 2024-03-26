
from .hpo_cr import HpoConceptRecognizer
from .column_mapper import ColumnMapper
from .simple_column_mapper import SimpleColumnMapper
from typing import List
import pandas as pd
import re

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
    def __init__(self, df:pd.DataFrame, observed:str, excluded:str, hpo_cr:HpoConceptRecognizer) -> None:
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


    def try_mapping_columns(self) -> List[ColumnMapper]:
        """As a side effect, this class initializes three lists of mapped, unmapped, and error columns

        :returns: A dictionary with successfully mapped columns
        :rtype: Dict[str,ColumnMapper]
        """
        simple_mapper_list = list()
        for col in self._df.columns:
            colname = str(col)
            result = re.search(r"(HP:\d+)", colname)
            if self._hpo_cr.contains_term_label(colname):
                hpo_term_list = self._hpo_cr.parse_cell(colname)
                hpo_term = hpo_term_list[0]
                scm = SimpleColumnMapper(column_name=colname,
                                        hpo_id=hpo_term.id,
                                        hpo_label=hpo_term.label,
                                        observed=self._observed,
                                        excluded=self._excluded)
                simple_mapper_list.append(scm)
            elif result:
                hpo_id = result.group(1)
                if self._hpo_cr.contains_term(hpo_id):
                    hterm = self._hpo_cr.get_term_from_id(hpo_id)
                    scm = SimpleColumnMapper(column_name=colname,
                                            hpo_id=hterm.id,
                                            hpo_label=hterm.label,
                                            observed=self._observed,
                                            excluded=self._excluded)
                    simple_mapper_list.append(scm)
                else:
                    self._unmapped_columns.append(colname)
            else:
                self._unmapped_columns.append(colname)
        self._mapped_columns = [scm.get_column_name() for scm in simple_mapper_list]
        return simple_mapper_list


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

    @staticmethod
    def from_map(column_name_to_hpo_label_map,
                observed='+',
                excluded='-') -> List[SimpleColumnMapper]:
        """
        Create SimpleColumnMapers from a map like this

           items = {
                'Developmental delay': ['Neurodevelopmental delay', 'HP:0012758'],
                'Regression': ['Cognitive regression', 'HP:0034332'],
                'Seizure': ['Seizure', 'HP:0001250'],
            }

        The keys are column names in the original file, and the values are used for creating the corresponding HPO terms

        :param column_name_to_hpo_label_map (_type_): map as described above
        :param observed: Symbol used to indicate observed. Defaults to '+'.
        :param excluded: Symbol used to indicate excluded. Defaults to '+'. '-'.
        :returns: list of SimpleColumnMapper
        :rtype: List[SimpleColumnMapper]
        """
        simple_mapper_list = list()
        for column_name, hpo_array in column_name_to_hpo_label_map.items():
            hpo_term_id = hpo_array[1]
            hpo_label = hpo_array[0]
            scm = SimpleColumnMapper(column_name=column_name,
                                    hpo_id=hpo_term_id,
                                    hpo_label=hpo_label,
                                    observed=observed,
                                    excluded=excluded)
            simple_mapper_list.append(scm)
        return simple_mapper_list




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
