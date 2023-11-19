import re
from collections import defaultdict
from enum import Enum

import pandas as pd

from .age_isoformater import AgeIsoFormater
from .constants import Constants

AgeEncodingType = Enum('AgeEncodingType', ['YEAR', 'ISO8601', 'YEAR_AND_MONTH', 'MONTH', 'CUSTOM', 'NOT_PROVIDED'])
ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"
# e.g., 14 y 8 m or 8 y
YEAR_AND_MONTH_REGEX = r"(\d+)\s*[Yy]\s*(\d+)\s*[Mm]"
YEAR_REGEX = r"(\d+)\s*[Yy]"
MONTH_REGEX = r"(\d+)\s*[Mm]"


class AgeColumnMapper:
    """
    Map a column that contains information about the age of individuals.

    Tables with information about genotype phenotype correlations typically
    contain a column with information about age. The columns often have formats
    such as 34 (integer with number of years or months) or 3Y2M (for three years 
    and two months). This mapper ingests data from such columns and transforms the
    contents into ISO 8601 strings (e.g., P4Y2M1D for 4 years, 2 months, and 1 day).
    
    """
    
    def __init__(self, ageEncodingType, column_name, string_to_iso_d=None) -> None:
       
        """
        :param ageEncodingType: Formatting convention used to represent the age
        :type ageEncodingType: one of Year (e.g. 42), ISO 8601 (e.g. P42Y2M), year/month (e.g. 42y2m)
        :param column_name: Name of the Age column in the original table
        :type column_name: str
        :param string_to_iso_d: dictionary from free text (input table) to ISO8601 strings
        :type string_to_iso_d: Dict[str,str], optional
        """

        if string_to_iso_d is None:
            string_to_iso_d = {}
        self._age_econding = ageEncodingType
        if column_name is None:
            raise ValueError("Must provide non-null column_name argument")
        self._column_name = column_name
        self._string_to_iso_d = string_to_iso_d

    def map_cell(self, cell_contents) -> str:

        """
        Map a single cell of the table

        :param cell_contents: The text contained in a single cell of the table
        :type cell_contents: can be a string or numerical type
        """
        
        contents = str(cell_contents)
        contents = contents.strip()
        if self._age_econding == AgeEncodingType.YEAR:
            isostring = self.get_iso8601_from_int_or_float_year(contents)
            if isostring is None:
                print(f"Could not parse {contents} as integer (year): {cell_contents}")
            return isostring
        elif self._age_econding == AgeEncodingType.YEAR_AND_MONTH:
            try:
                match = re.search(YEAR_AND_MONTH_REGEX, contents)
                if match:
                    years = int(match.group(1))
                    months = int(match.group(2))
                    return AgeIsoFormater.to_string(y=years, m=months)
                match = re.search(YEAR_REGEX, contents)
                if match:
                    years = int(match.group(1))
                    return AgeIsoFormater.to_string(y=years)
                match = re.search(MONTH_REGEX, contents)
                if match:
                    months = int(match.group(1))
                    return AgeIsoFormater.to_string(m=months)
            except ValueError as verr:
                print(f"Could not parse {contents} as year/month: {verr}")
                return Constants.NOT_PROVIDED
        elif self._age_econding == AgeEncodingType.MONTH:
            # assume month encoded by integer or float.
            return AgeIsoFormater.from_numerical_month(contents)
        elif self._age_econding == AgeEncodingType.ISO8601:
            match = re.search(ISO8601_REGEX, contents)
            if match:
                return contents
            else:
                print(f"Could not parse {contents} as ISO8601 period")
                return Constants.NOT_PROVIDED
        elif self._age_econding == AgeEncodingType.CUSTOM:
            return self._string_to_iso_d.get(cell_contents, Constants.NOT_PROVIDED)
        elif self._age_econding == AgeEncodingType.NOT_PROVIDED:
            return Constants.NOT_PROVIDED

    def get_iso8601_from_int_or_float_year(self, age) -> str:
        
        """
        Extract an iso8601 string for age recorded as a year (either an int such as 4 or a float such as 4.25 for P4Y3M)
        :param age: an int representing years or a float such as 2.5 for two and a half years
        :return: an ISO 8601 string such as P2Y6M
        """
        
        if isinstance(age, int):
            return f"P{age}Y"
        elif isinstance(age, float):
            age = str(age)
        elif not isinstance(age, str):
            raise ValueError(f"Malformed agestring {age}, type={type(age)}")
        int_or_float = r"(\d+)(\.\d+)?"
        p = re.compile(int_or_float)
        results = p.search(age).groups()
        if len(results) != 2:
            return Constants.NOT_PROVIDED
        if results[0] is None:
            return Constants.NOT_PROVIDED
        y = int(results[0])
        if results[1] is None:
            return f"P{y}Y"
        else:
            m = float(results[1])  # something like .25
            months = round(12 * m)
            return f"P{y}Y{months}M"

    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        preview_d = defaultdict(list)
        for index, value in column.items():
            preview_d[value] = self.map_cell(str(value))
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
    def not_provided():
        """Create an object for cases where Age is not provided.
        """
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.NOT_PROVIDED, column_name=Constants.NOT_PROVIDED)

    @staticmethod
    def by_year(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.YEAR, column_name=column_name)

    @staticmethod
    def by_year_and_month(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.YEAR_AND_MONTH, column_name=column_name)

    @staticmethod
    def by_month(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.MONTH, column_name=column_name)

    @staticmethod
    def iso8601(column_name):
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.ISO8601, column_name=column_name)

    @staticmethod
    def custom_dictionary(column_name, string_to_iso_d):
        """
        Create an AgeColumnMapper for free text input data such as Fetus, 1.5, birth, 51 days
        :param column_name: name of the age column in the input table
        :type column_name: str
        :param string_to_iso_d: dictionary with free text to ISO 8601
        :type string_to_iso_d: Dict[str,str)
        """
        return AgeColumnMapper(ageEncodingType=AgeEncodingType.CUSTOM,
                               column_name=column_name,
                               string_to_iso_d=string_to_iso_d)
