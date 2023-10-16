from .disease import Disease

from typing import Dict


class DiseaseIdColumnMapper:

    def __init__(self, column_name, disease_id_map):
        """
        Constructor

        :param column_name: name of column with disease identifier
        :type column_name: str
        :param disease_id_map: dictionary with key, free text for disease identifier/name, value Disease object
        :type disease_id_map: Dict[str, Disease]
        """
        self._column_name = column_name
        self._disease_id_dict = disease_id_map


    def map_cell(self, cell_contents):
        """
        :param cell_contents: contents of a cell of the origiinal table
        :type cell_contents: str
        :returns: corresponding Disease object
        :rtype: Disease
        :raises: ValueError if the cell contents cannot be mapped
        """
        if cell_contents not in self._disease_id_dict:
            raise ValueError(f"Could not map disease {cell_contents}")
        return self._disease_id_dict.get(cell_contents)

    def get_column_name(self):
        return self._column_name