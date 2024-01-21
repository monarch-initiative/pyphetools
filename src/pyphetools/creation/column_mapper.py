import abc
from typing import List
import pandas as pd
import re

class ColumnMapper(metaclass=abc.ABCMeta):
    """
    Abstract superclass for all Column Mapper classes, each of which applies a specific strategy to extracting HPO terms
    from columns of tables (e.g., supplemental files) representing cohorts of individuals with a given disease.
    """
    def __init__(self, column_name:str) -> None:
        """Constructor

        :param column_name: name of the column in the pandas DataFrame
        :type column_name: str
        """
        self._column_name = column_name

    @abc.abstractmethod
    def map_cell(self, cell_contents) -> List:
        """
        Map a cell to HPO Terms or other data
        """
        pass

    @abc.abstractmethod
    def preview_column(self, df:pd.DataFrame):
        """
        Show a preview of the entire column for review purposes

        :param df: the pandas DataFrame that contains the column (self._column_name)
        :type df: pd.DataFrame
        """
        pass

    @staticmethod
    def is_valid_iso8601(cell_contents):
        """Check for a match with iso8601 age (period)

        returns true for strings such as P6Y, P2M, P42Y1M2W1D etc.

        :returns: true iff the cell_contents represent an iso8601 age
        :rtype: bool
        """
        m = re.match(r"^P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?$", cell_contents)
        if m:
            return True
        else:
            return False

    def get_column_name(self):
        return self._column_name


