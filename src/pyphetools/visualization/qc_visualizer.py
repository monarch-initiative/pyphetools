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
    def __init__(self, cohort_validator:CohortValidator) -> None:
        self._ontology = cohort_validator.get_ontology()
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
        distinct_item_d = defaultdict(set)
        for vi in validated_individual_list:
            verrors = vi.get_validation_errors()
            total_validation_issues += vi.n_errors()
            for ve in verrors:
                error_count[ve.category] += 1
                distinct_item_d[ve.category].add(ve.term)
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
                para = f"<p>A total of {total_validation_issues} issues were fixed and no individual was removed from the cohort.</p>"
                html_lines.append(para)
            else:
                para = f"<p>A total of {total_validation_issues} issues were fixed and {n_removed} individuals were removed from the cohort because of irreparable errors. The cohort validator will return {n_error_free_i} individual objects without errors.</p>"
                html_lines.append(para)
                if "MALFORMED_LABEL" in distinct_item_d:
                    malformed_label_set = distinct_item_d.get("MALFORMED_LABEL")
                    if len(malformed_label_set) > 0:
                        malformed = "; ".join([t.hpo_term_and_id for t in malformed_label_set])
                        para = f"<p>The following malformed labels were found: {malformed}. These need to be corrected before continuing.</p>"
                        html_lines.append(para)
                if "REDUNDANT" in distinct_item_d:
                    redundant_label_set = distinct_item_d.get("REDUNDANT")
                    redundant = "; ".join([t.hpo_term_and_id for t in redundant_label_set])
                    para = f"<p>The following redundant terms were found: {redundant}. Redundant terms will be removed, keeping only one instance of the most specific term.</p>"
                    html_lines.append(para)
                if "CONFLICT" in distinct_item_d:
                    conflict_label_set = distinct_item_d.get("CONFLICT")
                    conflict = "; ".join([t.hpo_term_and_id for t in conflict_label_set])
                    para = f"<p>The following excluded terms were found to have a conflict with an observed descendent term: {conflict}. The ancestor terms will be removed.</p>"
                    html_lines.append(para)
                if "OBSERVED_AND_EXCLUDED" in distinct_item_d:
                    o_and_e_set = distinct_item_d.get("OBSERVED_AND_EXCLUDED")
                    o_and_e = "; ".join([t.hpo_term_and_id for t in o_and_e_set])
                    para = f"<p>The following terms were annotated as being both observed and excluded: {o_and_e}. This needs to be fixed manually.</p>"
                    html_lines.append(para)
                html_lines.append(self._get_unfixable_error_table())
        return "\n".join(html_lines)


    def _get_unfixable_error_table(self):
        v_individuals_with_unfixable = self._cohort_validator.get_validated_individuals_with_unfixable_errors()
        html_lines = []
        html_lines.append("<h2>Individuals with unfixable errors</h2>")
        errors = []
        for vi in v_individuals_with_unfixable:
            if vi.has_error():
                errors.extend(vi.get_validation_errors())
        errors = sorted(errors, key=lambda x : (x._error_level, x._category, x._message))
        header_fields = ValidationResult.get_header_fields()
        rows = [row.get_items_as_array() for row in errors]
        generator = HtmlTableGenerator(header_items=header_fields, rows=rows, caption="Error analysis")
        html_lines.append(generator.get_html())
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



