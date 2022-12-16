
from collections import defaultdict
from typing import List
import pandas as pd
from .individual_mapper import IndividualMapper
from .constants import *




class SexColumnMapper(IndividualMapper):
    def __init__(self, male_symbol, female_symbol, other_symbol=None, unknown_symbol=None) -> None:
        super().__init__(individual_type="sex")
        self._male_symbol    = male_symbol
        self._female_symbol  = female_symbol
        self._other_symbol   = other_symbol
        self._unknown_symbol = unknown_symbol
    
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
