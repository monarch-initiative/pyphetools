from typing import List
import hpotk
from ..validation.validation_result import ValidationResult
from ..validation.validated_individual import ValidatedIndividual
from ..validation.cohort_validator import CohortValidator

from .html_table_generator import HtmlTableGenerator

class QcVisualizer:
    def __init__(self, ontology:hpotk.MinimalOntology, cohort_validator:CohortValidator) -> None:
        self._ontology = ontology
        if not isinstance(cohort_validator, CohortValidator):
            raise ValueError(f"cohort_validator argument must be CohortValidator object but was {type(cohort_validator)}")
        self._cohort_validator = cohort_validator


    def to_html(self) -> str:
        validated_individual_list = self._cohort_validator.get_validated_individual_list()
        if not isinstance(validated_individual_list, list):
            raise ValueError(f"validated_individual_list argument must be a list but was {type(validated_individual_list)}")
        if len(validated_individual_list) == 0:
            raise ValueError(f"validated_individual_list argument was empty")
        if not isinstance(validated_individual_list[0], ValidatedIndividual):
            raise ValueError(f"validated_individual_list argument must be a list of ValidatedIndividual objects but was {type(validated_individual_list[0])}")
        html_lines = []
        n_individuals = len(validated_individual_list)
        n_individuals_with_errors = sum([1 for i in validated_individual_list if i.has_error()])
        html_lines.append("<h2>Cohort validation</h2>")
        if n_individuals_with_errors == 0:
            html_lines.append(f"<p>No errors found for the cohort with {n_individuals} individuals</p>")
        else:
            para = f"<p>Errors found with {n_individuals_with_errors} of {n_individuals} phenopackets.</p>"
            html_lines.append(para)
            errors = []
            for vi in validated_individual_list:
                if vi.has_error():
                    errors.extend(vi.get_validation_errors())
            errors = sorted(errors, key=lambda x : (x._error_level, x._category, x._message))
            header_fields = ValidationResult.get_header_fields()
            rows = [row.get_items_as_array() for row in errors]
            generator = HtmlTableGenerator(header_items=header_fields, rows=rows, caption="Error analysis")
            html_lines.append(generator.get_html())
        return "\n".join(html_lines)


