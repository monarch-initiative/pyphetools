from enum import Enum
from typing import List
from .column_mapper import ColumnMapper



IndividualSeriesType = Enum('IndividualSeriesType', ['AGE', 'SEX', 'IDENTIFIER'])

class IndividualMapper(ColumnMapper):
    """_summary_
    An 'abstract superclass' for SeriesMappers that deal with data about the individuals (age, sex, identifier)
    """
    def __init__(self, individual_type) -> None:
        super().__init__()
        if individual_type.lower() == 'age':
            self._individual_type = IndividualSeriesType.AGE
        elif individual_type.lower() == 'sex':
            self._individual_type = IndividualSeriesType.SEX
        elif  individual_type.lower() == 'indentifier':
            self._individual_type = IndividualSeriesType.IDENTIFIER
        else:
            raise ValueError(f"Did not recognize individual_type argument {individual_type}")
    
    def map_cell(self, cell_contents) -> List:
        raise NotImplementedError("Need to implement a subclass of IndividualMapper for map_cell")     


    def preview_column(self, column):
        raise NotImplementedError("Need to implement a subclass of IndividualMapper for preview_column") 
    
    def is_age_mapper(self):
        return self._individual_type == IndividualSeriesType.AGE  
    
    def is_identifier_mapper(self):
        return self._individual_type == IndividualSeriesType.IDENTIFIER  
    
    def is_sex_mapper(self):
        return self._individual_type == IndividualSeriesType.SEX  
   
            
        