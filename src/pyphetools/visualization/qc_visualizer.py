from typing import List
from collections import defaultdict
import hpotk
from ..validation.validation_result import ValidationResult
from ..validation.validated_individual import ValidatedIndividual
from ..validation.cohort_validator import CohortValidator

from .html_table_generator import HtmlTableGenerator




class QcElement:
    """Helper class to provide additional context and order for displaying summaries of Qc events

    :param level: ERROR, WARNING, or INFORMATION
    :type level: str
    :param category: from the ValidationResult categories
    :type category: str
    """
    def __init__(self, level, category) -> None:
        self._level = level
        self._category = category

    @property
    def level(self):
        return self._level

    @property
    def category(self):
        return self._category

    @staticmethod
    def get_qc_element_list():
        elements = []
        elements.append(QcElement(level="ERROR", category="CONFLICT"))
        elements.append(QcElement(level="ERROR", category="INSUFFICIENT_HPOS"))
        elements.append(QcElement(level="ERROR", category="INCORRECT_ALLELE_COUNT"))
        elements.append(QcElement(level="ERROR", category="INCORRECT_VARIANT_COUNT"))
        elements.append(QcElement(level="ERROR", category="MALFORMED_ID"))
        elements.append(QcElement(level="ERROR", category="MALFORMED_LABEL"))
        elements.append(QcElement(level="WARNING", category="REDUNDANT"))
        elements.append(QcElement(level="INFORMATION", category="NOT_MEASURED"))
        return elements



class QcVisualizer:
    """Class degigned to create HTML summaries of the validation/QC of a cohort
    :param ontology: HPO ontology
    :type ontology: hpotk.MinimalOntology
    :param cohort_validator: Validator object that checks all individuals in a cohort
    :type cohort_validator: CohortValidator
    """
    def __init__(self, ontology:hpotk.MinimalOntology, cohort_validator:CohortValidator) -> None:
        self._ontology = ontology
        if not isinstance(cohort_validator, CohortValidator):
            raise ValueError(f"cohort_validator argument must be CohortValidator object but was {type(cohort_validator)}")
        self._cohort_validator = cohort_validator


    def to_html(self) -> str:
        validated_individual_list = self._cohort_validator.get_validated_individual_list()
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

    def to_summary_html(self) -> str:
        validated_individual_list = self._get_validated_individuals()
        qc_element_list = QcElement.get_qc_element_list()
        error_count = defaultdict(int)
        total_validation_issues = 0
        for vi in validated_individual_list:
            verrors = vi.get_validation_errors()
            total_validation_issues += vi.n_errors()
            for ve in verrors:
                error_count[ve.category] += 1
        html_lines = []
        n_individuals = len(validated_individual_list)
        n_individuals_with_errors = sum([1 for i in validated_individual_list if i.has_error()])
        html_lines.append("<h2>Cohort validation</h2>")
        if n_individuals_with_errors == 0:
            html_lines.append(f"<p>No errors found for the cohort with {n_individuals} individuals</p>")
        else:
            para = f"<p>Errors found with {n_individuals_with_errors} of {n_individuals} phenopackets.</p>"
            html_lines.append(para)

            header_fields = ["Level", "Error category", "Count"]
            rows = []
            for elem in qc_element_list:
                if elem.category in error_count:
                    count = error_count.get(elem.category)
                    row = [elem.level, elem.category, str(count)]
                    rows.append(row)
            generator = HtmlTableGenerator(header_items=header_fields, rows=rows, caption="Error counts")
            html_lines.append(generator.get_html())
            n_removed = self._cohort_validator.n_removed_individuals()
            n_error_free_i = self._cohort_validator.n_error_free_individuals()
            if n_removed == 0:
                para = f"<p>A total of {total_validation_issues} were fixed and no individual was removed from the cohort.</p>"
            else:
                para = f"<p>A total of {total_validation_issues} issues were fixed and {n_removed} individuals were removed from the cohort because of irreparable errors. The cohort validator will return {n_error_free_i} individual objects without errors.</p>"
            html_lines.append(para)
        return "\n".join(html_lines)


    def _get_validated_individuals(self):
        validated_individual_list = self._cohort_validator.get_validated_individual_list()
        if not isinstance(validated_individual_list, list):
            raise ValueError(f"validated_individual_list argument must be a list but was {type(validated_individual_list)}")
        if len(validated_individual_list) == 0:
            raise ValueError(f"validated_individual_list argument was empty")
        if not isinstance(validated_individual_list[0], ValidatedIndividual):
            raise ValueError(f"validated_individual_list argument must be a list of ValidatedIndividual objects but was {type(validated_individual_list[0])}")
        return validated_individual_list



