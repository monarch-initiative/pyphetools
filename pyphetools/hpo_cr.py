



class HpoConceptRecognizer:
    """
    _summary_
    This class acts as an interface for classes that implement parse_cell to perform HPO-based concept recognition.
    """
    def __init__(self):
        pass
    
    def parse_cell(self):
        raise NotImplementedError("Need to implement a subclass of HpoConceptRecognizer for CR")
    
    def preview_column(self, column):
        raise NotImplementedError("Need to implement a subclass of HpoConceptRecognizer for preview_column")
        