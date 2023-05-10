from typing import List


class ColumnMapper:
    """
    Superclass for all Column Mapper classes, each of which applies a specific strategy to extracting HPO terms
    from columns of tables (e.g., supplemental files) representing cohorts of individuals with a given disease.
    """
    def __init__(self) -> None:
        pass

    def map_cell(self, cell_contents) -> List:
        raise NotImplementedError("Need to implement a subclass of ColumnMapper for map_cell")

    def preview_column(self, column):
        raise NotImplementedError("Need to implement a subclass of ColumnMapper for preview_column")
