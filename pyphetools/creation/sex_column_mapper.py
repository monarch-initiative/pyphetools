
from collections import defaultdict
from typing import List
import pandas as pd
from .constants import *




class SexColumnMapper():
    def __init__(self, male_symbol, female_symbol, column_name, other_symbol=None, unknown_symbol=None) -> None:
        self._male_symbol    = male_symbol
        self._female_symbol  = female_symbol
        self._other_symbol   = other_symbol
        self._unknown_symbol = unknown_symbol
        if column_name is None:
            raise ValueError("Must provide non-null column_name argument")
        self._column_name = column_name
    
    def map_cell(self, cell_contents) -> List:
        contents = cell_contents.strip()
        if contents == self._female_symbol:
            return FEMALE_SYMBOL
        elif contents == self._male_symbol:
            return MALE_SYMBOL
        elif contents == self._other_symbol:
            return OTHER_SEX_SYMBOL
        elif contents == self._unknown_symbol:
            return UNKOWN_SEX_SYMBOL
        else:
            print(f"Could not map sex symbol {contents}")
            return UNKOWN_SEX_SYMBOL        

    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for index, value in column.items():
            result  = self.map_cell(str(value))
            if result is None:
                dlist.append({"original column contents": value, "sex": "n/a"})
            else:
                dlist.append({"original column contents": value, "sex": result})
        return pd.DataFrame(dlist)
    

    def get_column_name(self):
        return self._column_name