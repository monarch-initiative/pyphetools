
import hpotk
from ..validation.validation_result import ValidationResult

class QcVisualizer:
    def __init__(self, ontology:hpotk.MinimalOntology) -> None:
        self._ontology = ontology


    def to_html(self, validation_result_list:list[ValidationResult]) -> str:
        pass