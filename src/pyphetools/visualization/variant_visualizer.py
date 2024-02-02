from typing import List
from collections import defaultdict
import hpotk
from ..creation.variant import Variant

from .html_table_generator import HtmlTableGenerator




class VariantVisualizer:
    """Helper class to provide additional context and order for displaying summaries of Qc events

    :param level: ERROR, WARNING, or INFORMATION
    :type level: str
    :param category: from the ValidationResult categories
    :type category: str
    """
    def __init__(self, variant_list:List[Variant]) -> None:
        self._variant_list = variant_list


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