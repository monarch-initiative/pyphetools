
from collections import defaultdict
from typing import List
import pandas as pd
import re


from enum import Enum

AgeEncodingType = Enum('AgeEncodingType', ['YEAR', 'ISO8601', 'YEAR_AND_MONTH', 'CUSTOM'])
ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"
# e.g., 14 y 8 m or 8 y
YEAR_AND_MONTH_REGEX = r"(\d+)\s*[Yy]\s*(\d+)\s*[Mm]"
YEAR_REGEX = r"(\d+)\s*[Yy]"
MONTH_REGEX = r"(\d+)\s*[Mm]"


class AgeColumnMapper():
    def __init__(self, ageEncodingType, column_name) -> None:
        self._age_econding = ageEncodingType
        if column_name is None:
            raise ValueError("Must provide non-null column_name argument")
        self._column_name = column_name
    
    
    def map_cell(self, cell_contents) -> str:
        if isinstance(cell_contents, str):
            contents = cell_contents.strip()
        else:
            contents = cell_contents
        if self._age_econding == AgeEncodingType.YEAR:
            isostring = self.get_iso8601_from_int_or_float_year(contents)
            if isostring is None:  
                print(f"Could not parse {contents} as integer (year): {verr}")
            return isostring
        if self._age_econding == AgeEncodingType.YEAR_AND_MONTH:
            try:
                match = re.search(YEAR_AND_MONTH_REGEX, contents)
                if match:
                    years = int(match.group(1))
                    months = int(match.group(2))
                    return f"P{years}Y{months}M"
                match = re.search(YEAR_REGEX, contents)
                if match:
                    years = int(match.group(1))
                    return f"P{years}Y"
                match = re.search(MONTH_REGEX, contents)
                if match:
                    months = int(match.group(1))
                    return f"P{months}M"
            except ValueError as verr:  
                print(f"Could not parse {contents} as year/month: {verr}")
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

    def get_iso8601_from_int_or_float_year(self, age_string) -> str:
        """
        Extract an iso8601 string for age recorded as a year (either an int such as 4 or a float such as 4.25 for P4Y3M)
        """
        if isinstance(age_string, int):
            return  f"P{age_string}Y"
        elif isinstance(age_string, float):
            age_string = str(age_string)
        elif not isinstance(age_string, str):
            raise ValueError(f"Malformed agestring {age_string}, type={type(age_string)}")
        int_or_float = r"(\d+)(\.\d+)?"
        p=re.compile(int_or_float)
        results = p.search(age_string).groups()
        if len(results) != 2:
            return None
        if results[0] is None:
            return None
        y = int(results[0])
        if results[1] is None:
            return  f"P{y}Y"
        else:
            m = float(results[1]) # something like .25
            months = round(12*m)
            return f"P{y}Y{months}M"



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
    def by_year_and_month(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.YEAR_AND_MONTH, column_name=column_name)
    
    @staticmethod
    def iso8601(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.ISO8601, column_name=column_name)

   