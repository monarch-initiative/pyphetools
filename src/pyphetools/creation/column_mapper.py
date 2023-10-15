import abc
from typing import List


class ColumnMapper(metaclass=abc.ABCMeta):
    """
    Abstract superclass for all Column Mapper classes, each of which applies a specific strategy to extracting HPO terms
    from columns of tables (e.g., supplemental files) representing cohorts of individuals with a given disease.
    """
    def __init__(self) -> None:
        pass
    
    @abc.abstractmethod
    def map_cell(self, cell_contents) -> List:
        """
        Map a cell to HPO Terms or other data
        """
        pass

    @abc.abstractmethod
    def preview_column(self, column):
        """
        Show a previous of the entire column
        """
        pass

