import re
from collections import defaultdict
from enum import Enum
import abc
import math
import pandas as pd

from .age_isoformater import AgeIsoFormater
from .pyphetools_age import HPO_ONSET_TERMS, PyPheToolsAge, IsoAge, NoneAge, GestationalAge, HpoAge
from .constants import Constants

ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"
# e.g., 14 y 8 m or 8 y
YEAR_AND_MONTH_REGEX = r"(\d+)\s*[Yy]\s*(\d+)\s*[Mm]"
YEAR_REGEX = r"(\d+)\s*[Yy]"
MONTH_REGEX = r"(\d+)\s*[Mm]"


class AgeColumnMapper(metaclass=abc.ABCMeta):
    """
    Map a column that contains information about the age of individuals.

    Tables with information about genotype phenotype correlations typically
    contain a column with information about age. The columns often have formats
    such as 34 (integer with number of years or months) or 3Y2M (for three years
    and two months). This mapper ingests data from such columns and transforms the
    contents into ISO 8601 strings (e.g., P4Y2M1D for 4 years, 2 months, and 1 day).

    There are many different formats to be parsed and so we have a small class hierarchy

    """

    def __init__(self, column_name:str, string_to_iso_d=None) -> None:
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
        if column_name is None:
            raise ValueError("Must provide non-null column_name argument")
        self._column_name = column_name
        self._string_to_iso_d = string_to_iso_d
        self._erroneous_input_counter = defaultdict(int)

    @abc.abstractmethod
    def map_cell(self, cell_contents) -> PyPheToolsAge:

        """
        Map a single cell of the table

        :param cell_contents: The text contained in a single cell of the table
        :type cell_contents: can be a string or numerical type
        """
        pass

    def _clean_contents(self, cell_contents):
        contents = str(cell_contents)
        contents = contents.strip()
        return contents

    def preview_column(self, df:pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df argument must be pandas DataFrame, but was {type(column)}")
        preview_d = {}
        column = df[self.get_column_name()]
        for _, column_contents in column.items():
            pyphetools_age = self.map_cell(str(column_contents))
            preview_d[pyphetools_age.age_string] = column_contents
        dlist = []
        for k, v in preview_d.items():
            if v is None:
                dlist.append({"original column contents": k, "age": "n/a"})
            else:
                dlist.append({"original column contents": k, "age": v})
        return pd.DataFrame(dlist)

    def get_column_name(self) -> str:
        return self._column_name

    def has_error(self) -> bool:
        return len(self._erroneous_input_counter) > 0

    def error_summary(self):
        items = []
        for k, v in self._erroneous_input_counter.items():
            items.append(f"{k} (n={v})")
        return f"Could not parse the following as ISO8601 ages: {', '.join(items)}"


    @staticmethod
    def not_provided():
        """Create an object for cases where Age is not provided.
        """
        return NotProvidedAgeColumnMapper(column_name=Constants.NOT_PROVIDED)

    @staticmethod
    def by_year(column_name) -> "AgeColumnMapper":
        return YearAgeColumnMapper(column_name=column_name)

    @staticmethod
    def by_year_and_month(column_name) -> "AgeColumnMapper":
        return YearMonthAgeColumnMapper(column_name=column_name)

    @staticmethod
    def by_month(column_name) -> "AgeColumnMapper":
        return MonthAgeColumnMapper(column_name=column_name)

    @staticmethod
    def iso8601(column_name) -> "AgeColumnMapper":
        return Iso8601AgeColumnMapper(column_name=column_name)

    @staticmethod
    def hpo_onset(column_name) -> "AgeColumnMapper":
        return HpoAgeColumnMapper(column_name=column_name)

    @staticmethod
    def custom_dictionary(column_name, string_to_iso_d):
        """
        Create an AgeColumnMapper for free text input data such as Fetus, 1.5, birth, 51 days
        :param column_name: name of the age column in the input table
        :type column_name: str
        :param string_to_iso_d: dictionary with free text to ISO 8601
        :type string_to_iso_d: Dict[str,str)
        """
        return CustomAgeColumnMapper(column_name=column_name,
                            string_to_iso_d=string_to_iso_d)



class Iso8601AgeColumnMapper(AgeColumnMapper):
    """Mapper for entries such as P1Y2M (ISO 8601 period to represent age)

    """
    def __init__(self, column_name) -> None:
        super().__init__(column_name=column_name)

    def map_cell(self, cell_contents) -> PyPheToolsAge:
        contents = self._clean_contents(cell_contents=cell_contents)
        match = re.search(ISO8601_REGEX, contents)
        if match:
            return IsoAge.from_iso8601(contents)
        else:
            self._erroneous_input_counter[contents] += 1
            return NoneAge(contents)


class YearMonthAgeColumnMapper(AgeColumnMapper):
    """Mapper for entries such as P1Y2M (ISO 8601 period to represent age)

    """
    def __init__(self, column_name) -> None:
        super().__init__(column_name=column_name)

    def map_cell(self, cell_contents) -> PyPheToolsAge:
        contents = self._clean_contents(cell_contents=cell_contents)
        try:
            match = re.search(YEAR_AND_MONTH_REGEX, contents)
            if match:
                years = int(match.group(1))
                months = int(match.group(2))
                age_string = f"P{years}Y{months}M"
                return IsoAge(y=years, m=months, age_string=age_string)
            match = re.search(YEAR_REGEX, contents)
            if match:
                years = int(match.group(1))
                age_string = f"P{years}Y"
                return IsoAge(y=years, age_string=age_string)
            match = re.search(MONTH_REGEX, contents)
            if match:
                months = int(match.group(1))
                age_string = f"P{months}M"
                return IsoAge(m=months, age_string=age_string)
        except ValueError as verr:
            print(f"Could not parse {cell_contents} as year/month: {verr}")
            return NoneAge(contents)

class MonthAgeColumnMapper(AgeColumnMapper):
    """Mapper for entries such as P1Y2M (ISO 8601 period to represent age)

    """
    def __init__(self, column_name) -> None:
        super().__init__(column_name=column_name)

    def map_cell(self, cell_contents) -> PyPheToolsAge:
        # assume month encoded by integer or float.
        contents = self._clean_contents(cell_contents=cell_contents)
        month = str(contents)
        if month.isdigit():
            full_months = int(month)
            days = 0
            age_string = AgeIsoFormater.from_numerical_month(full_months)
            return IsoAge(m=full_months, age_string=age_string)
        elif month.replace('.', '', 1).isdigit() and month.count('.') < 2:
            # a float such as 0.9 (months)
            months = float(month)
            avg_num_days_in_month = 30.437
            floor_months = math.floor(months)
            if floor_months == 0.0:
                days = int(months * avg_num_days_in_month)
                full_months = 0
                age_string = f"P{days}D"
                return IsoAge(d=days, age_string=age_string)
            else:
                remainder = months - floor_months
                full_months = int(months - remainder)
                days = int(remainder * avg_num_days_in_month)
                age_string = f"P{full_months}M{days}D"
                return IsoAge(m=full_months, d=days, age_string=age_string)
        else:
            return NoneAge("na")



class YearAgeColumnMapper(AgeColumnMapper):

    def __init__(self, column_name) -> None:
        super().__init__(column_name=column_name)

    def map_cell(self, cell_contents) -> PyPheToolsAge:
        """
        Extract an iso8601 string for age recorded as a year (either an int such as 4 or a float such as 4.25 for P4Y3M)
        :param age: an int representing years or a float such as 2.5 for two and a half years
        :return: an ISO 8601 string such as P2Y6M
        """
        if isinstance(cell_contents, int):
            return IsoAge(y=cell_contents, age_string=contents)
        elif isinstance(cell_contents, float):
            age = str(age)
        elif not isinstance(cell_contents, str):
            raise ValueError(f"Malformed agestring {age}, type={type(age)}")
        contents = self._clean_contents(cell_contents=cell_contents)
        int_or_float = r"(\d+)(\.\d+)?"
        p = re.compile(int_or_float)
        results = p.search(contents).groups()
        if len(results) != 2:
            return NoneAge(contents)
        if results[0] is None:
            return NoneAge(contents)
        y = int(results[0])
        if results[1] is None:
            return IsoAge(y=y, age_string=f"P{y}Y")
        else:
            m = float(results[1])  # something like .25
            months = round(12 * m)
            return IsoAge(y=y, m=months, age_string=f"P{y}Y{months}M")


class CustomAgeColumnMapper(AgeColumnMapper):
    """Mapper for custom maps. For instance, the key might be "4y and 2mt" and the value would be "P4Y2M"
    It is prefered to manually adjust the age column in the input file to valid iso8601 statements, but this
    class can be used if required.
    """
    def __init__(self, column_name:str, string_to_iso_d) -> None:
        super().__init__(column_name=column_name)
        self._string_to_iso_d = string_to_iso_d

    def map_cell(self, cell_contents) -> PyPheToolsAge:
        if cell_contents not in self._string_to_iso_d:
            print(f"[WARNING] Could not find \"{cell_contents}\" in custom dictionary")
            return NoneAge(cell_contents)
        iso8601 = self._string_to_iso_d.get(cell_contents, Constants.NOT_PROVIDED)
        return IsoAge.from_iso8601(iso8601)

class NotProvidedAgeColumnMapper(AgeColumnMapper):
    """Mapper if there is no information

    """
    def __init__(self, column_name:str) -> None:
        super().__init__(column_name=column_name)

    def map_cell(self, cell_contents) -> str:
        if cell_contents is None or math.isnan(cell_contents):
            cell_contents = "na"
        contents = self._clean_contents(cell_contents=cell_contents)
        return NoneAge(age_string=contents)


class HpoAgeColumnMapper(AgeColumnMapper):
    """Mapper for HPO Onset terms. The cells must contain labels of a valid HPO onset term.
    If the value is valid, it is returned in the expectation that PyPheToolsAge will do the
    rest of the work.

    """
    def __init__(self, column_name:str) -> None:
        super().__init__(column_name=column_name)

    def map_cell(self, cell_contents) -> PyPheToolsAge:
        contents = self._clean_contents(cell_contents=cell_contents)
        if contents in HPO_ONSET_TERMS:
            return HpoAge(hpo_onset_label=contents)
        else:
            self._erroneous_input_counter[contents] += 1
            return NoneAge(cell_contents)