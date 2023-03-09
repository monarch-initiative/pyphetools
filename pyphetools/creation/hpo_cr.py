
from typing import List
from .hp_term import HpTerm


class HpoConceptRecognizer:
    """
    _summary_
    This class acts as an interface for classes that implement parse_cell to perform HPO-based concept recognition.
    """
    def __init__(self):
        pass
    
    def parse_cell(self, cell_contents, custom_d=None)-> List[HpTerm]:
        raise NotImplementedError("Need to implement a subclass of HpoConceptRecognizer for CR")    

    def get_term_from_id(self, id) -> HpTerm:
        raise NotImplementedError("Need to implement a subclass of HpoConceptRecognizer for CR")   
    
    def get_term_from_label(self, label) -> HpTerm:
        raise NotImplementedError("Need to implement a subclass of HpoConceptRecognizer for CR")   
    
    def initialize_simple_column_maps(self, column_name_to_hpo_label_map, observed, excluded, non_measured=None):
        raise NotImplementedError("Need to implement a subclass of HpoConceptRecognizer for CR")   
