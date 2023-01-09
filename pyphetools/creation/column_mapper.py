from collections import defaultdict
from typing import List
import pandas as pd
from .hpo_cr import HpoConceptRecognizer


class ColumnMapper:
    def __init__(self) -> None:
        pass


    def map_cell(self, cell_contents) -> List:
        raise NotImplementedError("Need to implement a subclass of ColumnMapper for map_cell")     


    def preview_column(self, column):
        raise NotImplementedError("Need to implement a subclass of ColumnMapper for preview_column")    
   
            
        