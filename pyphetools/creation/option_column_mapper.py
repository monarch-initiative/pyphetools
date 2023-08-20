from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer
from typing import List
import pandas as pd
import re
from collections import defaultdict

class OptionColumnMapper(ColumnMapper):
    
    def __init__(self, concept_recognizer, option_d, excluded_d=None):
        """Mapper to be used if the column has a set of defined items but text mining is not required.

        Args:
            option_d (dict): key: item (e.g., MVP) in original publication; value: corresponding HPO label, e.g. Mitral Valve Prolapse
            excluded_d: key: excluded string, value: excluded HPO term label
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
        if excluded_d is None:
            excluded_d = defaultdict()
        self._excluded_d = excluded_d
        
    def map_cell(self, cell_contents) -> List[HpTerm]:
        """Map cell contents using the option dictionary 
        
        Args:
            cell_contents (str): contents of one table cell
        """
        results = []
        contents = cell_contents.strip()
        if contents in self._excluded_d:
            excluded_hpo_label = self._excluded_d.get(contents)
            term = self._hpo_cr.get_term_from_label(label=excluded_hpo_label)
            term.excluded()
            results.append(term)
            return results
        delimiters = ',;|/'
        regex_pattern = '|'.join(map(re.escape, delimiters))
        chunks = re.split(regex_pattern, contents)
        chunks = [chunk.strip() for chunk in chunks]

        hpo_labels = []
        for c in chunks:
            for my_key, my_label in self._option_d.items():
                if my_key in c:
                    if isinstance(my_label, list):
                        for itm in my_label:
                            hpo_labels.append(itm)
                    else:
                        hpo_labels.append(my_label)
        for label in hpo_labels:    
            term = self._hpo_cr.get_term_from_label(label=label)
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
    
    @staticmethod
    def autoformat(df: pd.DataFrame, concept_recognizer, delimiter=",", omit_columns=None) -> str:
        """Autoformat code from the colums so that we can easily copy-paste and change it.
        This method intends to save time by preformatting code the create OptionMappers.
        
        Args:
            df: data frame with the data about the individuals
            concept_recognizer: HpoConceptRecognizer for text mining
            delimiter: the string used to delimit individual items in a cell (default: comma)
            omit_columns: names of columns to omit from this search
        Return:
            a string that should be displayed using a print() command in the notebook
        """  
        lines = []
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"argument \"df\" must be a pandas DataFrame but was {type(df)}")
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer arg must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        if omit_columns is None:
            omit_columns = set()
        elif isinstance(omit_columns, list):
            omit_columns = set(list)
        elif not isinstance(omit_columns, set):
            raise ValueError(f"If passed, omit_columns argument must be set or list but was {type(omit_columns)}")
        # df.shape[1] gives us the number of columns
        for y in range(df.shape[1]):
            if y in omit_columns:
                continue
            temp_dict = {}
            for i in range(len(df)):
                if len(str(df.iloc[i, y])) > 1:
                    for entry in str(df.iloc[i, y]).split(delimiter):
                        hpo_term = concept_recognizer.parse_cell(entry.strip())
                        if len(hpo_term) > 0:
                            temp_dict[entry.strip()] = hpo_term[0].label                
                        else:
                            temp_dict[entry.strip()] = 'PLACEHOLDER'
            col_name = str(df.columns[y]).lower().replace(", ","_").replace(' ', '_')
            col_name = col_name.lower()
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
            lines.append(f"{col_name}Mapper = OptionColumnMapper(concept_recognizer=hpo_cr, option_d={items_d_name})")
            lines.append(f"{col_name}Mapper.preview_column(df['" + str(df.columns[y]) + "'])")
            lines.append(f"column_mapper_d['{str(df.columns[y])}'] = {col_name}Mapper")
            lines.append("")
        return "\n".join(lines)
        
   