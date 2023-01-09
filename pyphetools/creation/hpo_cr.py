
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