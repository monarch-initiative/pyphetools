from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer
from typing import List, Set
import pandas as pd
import re
from collections import defaultdict


class OptionColumnMapper(ColumnMapper):
    """Class to map the contents of a table cell to one or more options (HPO terms)

    This mapper should be used if the column has a set of multiple defined items (strings) representing HPO terms.
    The excluded_d argument should be used if the column includes excluded (negated) HPO terms
    :param column_name: name of the column in the pandas DataFrame
    :type column_name: str
    :param concept_recognizer: HpoConceptRecognizer for text mining
    :type  concept_recognizer: pyphetools.creation.HpoConceptRecognizer
    :param option_d: dictionary with key: string corresponding to original table, value: corresponding HPO term label
    :type option_d:TypedDict[str,str]
    :param excluded_d: dictionary with key: similar to option_d but for excluded HPO terms, optional
    :type excluded_d:TypedDict[str,str]

    :param omitSet: set of strings to be excluded from concept recognition
    :type omitSet: Set[str]
    """

    def __init__(self, column_name:str, concept_recognizer, option_d, excluded_d=None, omitSet:Set[str]=None):
        """Constructor
        """
        super().__init__(column_name=column_name)
        # Either have self._option_d be an empty dictionary or it must be a valid dictionary
        if option_d is None or not isinstance(option_d, dict):
            raise ValueError(f"option_d argument must be dictionary but was {type(option_d)}")
        self._option_d = option_d
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer arg must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._hpo_cr = concept_recognizer
        if excluded_d is None:
            excluded_d = defaultdict()
        self._excluded_d = excluded_d
        if omitSet is None:
            omitSet = set()
        elif not isinstance(omitSet, set):
            raise ValueError(f"argument 'omitSet' must be a Python set but was {type(omitSet)}")
        self._omit_set = omitSet


    def map_cell(self, cell_contents) -> List[HpTerm]:
        """parse a single table cell

        :param cell_contents: contents of a cell of the original file
        :type cell_contents: str
        :returns: list of HPO matches
        :rtype: List[HpTerm]
        """
        for excl in self._omit_set:
            cell_contents = cell_contents.replace(excl, " ")
        # results is a list of HpTerm objects
        results = []
        if self._excluded_d is not None and len(self._excluded_d) > 0:
            excluded_results = self._hpo_cr.parse_cell_for_exact_matches(cell_text=cell_contents, custom_d=self._excluded_d)
            if excluded_results is not None and len(excluded_results) > 0:
                for er in excluded_results:
                    er.excluded()
                    results.append(er)
                    # remove excluded terms from contents
                    cell_contents = cell_contents.replace(er.label.lower(), " ")
        results_obs = self._hpo_cr.parse_cell(cell_contents=cell_contents, custom_d=self._option_d)
        results.extend(results_obs)
        return results

    def preview_column(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Generate a pandas dataframe with a summary of parsing of the entire column

        This method is intended for use in developing the code for ETL of an input column.
        It is only needed for development and debugging.

        :param column: A single column from the input table
        :type column: pd.Series
        :returns: a pandas dataframe with one row for each entry of the input column
        :rtype: pd.DataFrame
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be pandas DataFrame, but was {type(column)}")
        column = df[self._column_name]
        mapping_counter = defaultdict(int)
        for _, value in column.items():
            cell_contents = str(value)
            term_list = self.map_cell(cell_contents)
            for hpterm in term_list:
                mapped = f"{hpterm.hpo_term_and_id} ({hpterm.display_value})"
                mapping_counter[mapped] += 1
        dlist = []
        for k, v in mapping_counter.items():
            d = {"mapping": k, "count": str(v)}
            dlist.append(d)
        return pd.DataFrame(dlist)

    @staticmethod
    def autoformat(df: pd.DataFrame, hpo_cr:HpoConceptRecognizer, delimiter:str=",", omit_columns:List[str]=None) -> str:
        """Autoformat code from the columns so that we can easily copy-paste and change it.

        This method intends to save time by preformatting code the create OptionMappers. The following commands
        will print out skeleton Python code that can be easily adapted to create a mapper.

            result = OptionColumnMapper.autoformat(df=dft, concept_recognizer=hpo_cr, delimiter=",")
            print(result)

        :param df: data frame with the data about the individuals
        :type df: pd.DataFrame
        :param concept_recognizer: HpoConceptRecognizer for text mining
        :type  concept_recognizer: pyphetools.creation.HpoConceptRecognizer
        :param delimiter: the string used to delimit individual items in a cell (default: comma)
        :type delimiter: str
        :param omit_columns: names of columns to omit from this search
        :type omit_columns: List[str]
        :param df_name: name of the variable that corresponds to the dataframe
        :type df_name: str
        :returns: a string that should be displayed using a print() command in the notebook - has info about automatically mapped columns
        :rtype: str
        """
        lines = []
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"argument \"df\" must be a pandas DataFrame but was {type(df)}")
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(f"concept_recognizer arg must be HpoConceptRecognizer but was {type(hpo_cr)}")
        if omit_columns is None:
            omit_columns = set()
        elif isinstance(omit_columns, list):
            omit_columns = set(omit_columns)
        elif not isinstance(omit_columns, set):
            raise ValueError(f"If passed, omit_columns argument must be set or list but was {type(omit_columns)}")
        # df.shape[1] gives us the number of columns
        for y in range(df.shape[1]):
            original_column_name = str(df.columns[y])
            clean_column_name = str(df.columns[y]).lower().replace(", ","_").replace(' ', '_').replace("/", "_")
            col_name = clean_column_name.lower()
            if original_column_name in omit_columns:
                continue
            temp_dict = {}
            for i in range(len(df)):
                if len(str(df.iloc[i, y])) > 1:
                    for entry in str(df.iloc[i, y]).split(delimiter):
                        hpo_term = hpo_cr.parse_cell(entry.strip())
                        if len(hpo_term) > 0:
                            temp_dict[entry.strip()] = hpo_term[0].label
                        else:
                            temp_dict[entry.strip()] = 'PLACEHOLDER'

            # skip columns that are unlikely to be interesting for the OptionColumnMapper
            if "patient" in col_name:
                continue
            if "family" in col_name:
                continue
            if "gender" in col_name:
                continue
            if "mutation" in col_name or "varia" in col_name:
                continue
            if "age" == col_name or "sex" == col_name or "gender" == col_name:
                continue
            items_d_name = f"{col_name}_d"
            items_d_string = str(temp_dict).replace(',', ',\n')
            lines.append(f"{items_d_name} = {items_d_string}")
            lines.append("excluded = {}")
            lines.append(f"{col_name}Mapper = OptionColumnMapper(column_name=\"{original_column_name}\", concept_recognizer=hpo_cr, option_d={items_d_name}, excluded_d=excluded)")
            lines.append(f"column_mapper_list.append({col_name}Mapper)")
            lines.append(f"{col_name}Mapper.preview_column(df)")

            lines.append("")
        return "\n".join(lines)

