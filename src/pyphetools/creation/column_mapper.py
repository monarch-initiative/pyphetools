import abc
from typing import List


class ColumnMapper(metaclass=abc.ABCMeta):
    """
    Superclass for all Column Mapper classes, each of which applies a specific strategy to extracting HPO terms
    from columns of tables (e.g., supplemental files) representing cohorts of individuals with a given disease.
    """
    def __init__(self) -> None:
        pass
    
    @abc.abstractmethod
    def map_cell(self, cell_contents) -> List:
        pass

    @abc.abstractmethod
    def preview_column(self, column):
        pass

