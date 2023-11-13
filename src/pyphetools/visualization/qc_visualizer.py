from typing import List
import hpotk
from ..validation.validation_result import ValidationResult
from ..validation.validated_individual import ValidatedIndividual

class QcVisualizer:
    def __init__(self, ontology:hpotk.MinimalOntology) -> None:
        self._ontology = ontology


    def to_html(self, validated_individual_list:List[ValidatedIndividual]) -> str:
        html_lines = []
        n_individuals = len(validated_individual_list)
        n_individuals_with_errors = sum([1 for i in validated_individual_list if i.has_error()])
        html_lines.append("<h2>Cohort validation</h2>")
        if n_individuals_with_errors == 0:
            html_lines.append(f"<p>No errors found for the cohort with {n_individuals} individuals</p>")
            return "\n".join(html_lines)
        else:
            return "HELP"
