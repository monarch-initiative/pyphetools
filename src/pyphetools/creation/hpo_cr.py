import abc
from typing import List

from .hp_term import HpTerm


class HpoConceptRecognizer(metaclass=abc.ABCMeta):
    """
    This abstract class acts as an interface for classes that implement parse_cell to perform HPO-based concept recognition.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse_cell(self, cell_contents, custom_d=None) -> List[HpTerm]:
        """
        parse HPO Terms form the contents of a cell of the original table

        :param cell_contents: a cell of the original table
        :type cell_contents: str
        :param custom_d: a dictionary with keys for strings in the original table and their mappings to HPO labels
        :type custom_d: Dict[str,str], optional
        """
        pass

    @abc.abstractmethod
    def get_term_from_id(self, hpo_id) -> HpTerm:
        """
        :param hpo_id: an HPO identifier, e.g., HP:0004372
        :type hpo_id: str
        :returns: corresponding HPO term
        :rtype: HpTerm
        """
        pass

    @abc.abstractmethod
    def get_term_from_label(self, label) -> HpTerm:
        """
        :param label: an HPO label, e.g., Arachnodactyly
        :type label: str
        :returns: corresponding HPO term
        :rtype: HpTerm
        """
        pass

    @abc.abstractmethod
    def initialize_simple_column_maps(self, column_name_to_hpo_label_map, observed, excluded, non_measured=None):
        """
        Create a dictionary of SimpleColumnMappers
        """
        pass

    @abc.abstractmethod
    def get_hpo_ontology(self):
        """
        :returns: a reference to the HPO-toolkit Ontology object for the HPO
        :rtype: hpotk.MinimalOntology
        """
        pass
