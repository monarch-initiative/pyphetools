
import pandas as pd
from typing import Optional
from .age_isoformater import AgeIsoFormater
from .constants import Constants

from pyphetools.pp.v202 import VitalStatus as pptVitalStatus
from pyphetools.pp.v202 import TimeElement as pptTimeElement
from pyphetools.pp.v202 import Age as pptAge


class AgeOfDeathColumnMapper:

    def __init__(self, column_name, string_to_iso_d=None) -> None:
        """
        :param column_name: Name of the Age of death column in the original table
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

    def map_cell_to_vital_status(self, cell_contents) -> Optional[pptVitalStatus]:

        """
        Map a single cell of the table

        :param cell_contents: The text contained in a single cell of the table
        :type cell_contents: can be a string or numerical type
        """

        contents = str(cell_contents)
        if contents not in self._string_to_iso_d:
            return None
        # Wrap the Age (iso8601) in a TimeElement.
        iso_age = pptAge(self._string_to_iso_d.get(contents))
        telem = pptTimeElement(iso_age)
        vstatus = pptVitalStatus(status=pptVitalStatus.Status.DECEASED, time_of_death=telem)
        return vstatus

    @property
    def column_name(self):
        return self._column_name
