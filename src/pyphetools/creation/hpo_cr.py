import abc
from typing import List
from .hp_term import HpTerm


class HpoConceptRecognizer(metaclass=abc.ABCMeta):
    """
    _summary_
    This class acts as an interface for classes that implement parse_cell to perform HPO-based concept recognition.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse_cell(self, cell_contents, custom_d=None) -> List[HpTerm]:
        pass

    @abc.abstractmethod
    def get_term_from_id(self, hpo_id) -> HpTerm:
        pass

    @abc.abstractmethod
    def get_term_from_label(self, label) -> HpTerm:
        pass

    @abc.abstractmethod
    def initialize_simple_column_maps(self, column_name_to_hpo_label_map, observed, excluded, non_measured=None):
        pass
