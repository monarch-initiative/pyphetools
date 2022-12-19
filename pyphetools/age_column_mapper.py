
from collections import defaultdict
from typing import List
import pandas as pd
import re


from enum import Enum

AgeEncodingType = Enum('AgeEncodingType', ['YEAR', 'ISO8601', 'CUSTOM'])
ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"


class AgeColumnMapper():
    def __init__(self, ageEncodingType, column_name) -> None:
        self._age_econding = ageEncodingType
        if column_name is None:
            raise ValueError("Must provide non-null column_name argument")
        self._column_name = column_name
    
    
    def map_cell(self, cell_contents) -> List:
        if isinstance(cell_contents, str):
            contents = cell_contents.strip()
        else:
            contents = cell_contents
        if self._age_econding == AgeEncodingType.YEAR:
            try:
                years = int(contents)
                return f"P{years}Y"
            except ValueError as verr:  
                print(f"Could not parse {contents} as integer (year): {verr}")
                return None
        elif self._age_econding == AgeEncodingType.ISO8601:
            match = re.search(ISO8601_REGEX, contents)
            if match:
                return contents
            else:
                print(f"Could not parse {contents} as ISO8601 period")
                return None
        elif self._age_econding == AgeEncodingType.CUSTOM:
            raise ValueError("TODO NOT IMPLEMENTED YET")   



    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        preview_d = defaultdict(list)
        for index, value in column.items():
            preview_d[value]  = self.map_cell(str(value))
        dlist = []
        for k, v in preview_d.items():
            if v is None:
                dlist.append({"original column contents": k, "age": "n/a"})
            else:
                dlist.append({"original column contents": k, "age": v})
        return pd.DataFrame(dlist)
    
    def get_column_name(self):
        return self._column_name
    
    @staticmethod
    def by_year(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.YEAR, column_name=column_name)
    
    @staticmethod
    def iso8601(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.ISO8601, column_name=column_name)

   