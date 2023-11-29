from enum import IntEnum
from typing import List, Optional

from ..creation.hp_term import HpTerm
from ..creation.allelic_requirement import AllelicRequirement


class ErrorLevel(IntEnum):
    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    UNKNOWN = 4



class Category(IntEnum):
    """
    These are the five types of error that we can identify.
    - REDUNDANT: A term and an ancestor of the term are both used to annotate the same individual
    - CONFLICT: A term is used to annotate an individual but an ancestor of the term is excluded in the same individual
    - INSUFFICIENT_HPOS: The number of HPO terms used to annotate an individual is less than the threshold value
    - INSUFFICIENT_ALLELES:  The number of alleles used to annotate an individual is less than the threshold value
    - INSUFFICIENT_VARIANTS:  The number of variants used to annotate an individual is less than the threshold value
    """
    REDUNDANT = 1
    CONFLICT = 2
    INSUFFICIENT_HPOS = 3
    INCORRECT_ALLELE_COUNT = 4
    INCORRECT_VARIANT_COUNT = 5
    MALFORMED_ID = 6
    MALFORMED_LABEL = 7
    NOT_MEASURED = 8
    OBSERVED_AND_EXCLUDED = 9
    UNKNOWN = 10


class ValidationResult:
    """
    A helper class to store the results of validation
    :param phenopacket_id: Identifier of the phenopacket being validated
    :type phenopacket_id: str
    :param message: description of the error/warning
    :type message: str
    :param errorlevel: whether this result is an error or a warning
    :type errorlevel: ErrorLevel
    :param category: type of QcError
    :type category: Category
    :param term: HpTerm that caused the error
    :type term: HpTerm

    """
    def __init__(self, phenopacket_id:str, message:str, errorlevel:ErrorLevel, category:Category, term:HpTerm=None):
        self._phenopacket_id = phenopacket_id
        self._message = message
        self._error_level = errorlevel
        self._category = category
        self._term = term

    @property
    def id(self):
        return self._phenopacket_id

    @property
    def message(self) -> str:
        """
        :returns: description of the cause of ValidationResult
        :rtype: str
        """
        return self._message

    @property
    def error_level(self)-> str:
        """
        :returns: the name of the ErrorLevel this ValidationResult is about
        :rtype: str
        """
        return self._error_level.name

    @property
    def term(self) -> Optional[HpTerm]:
        """
        :returns: A string representation of the HPO term this ValidationResult is about, if applicable, or empty string
        :rtype: Optional[str]
        """
        return self._term

    @property
    def category(self) -> str:
        """
        :returns: the name of the Category this ValidationResult is about
        :rtype: str
        """
        return self._category.name

    def is_error(self) -> bool:
        return self._error_level == ErrorLevel.ERROR

    def is_warning(self) -> bool:
        return self._error_level == ErrorLevel.WARNING

    def get_items_as_array(self) -> List[str]:
        """
        :returns: A list of items (strings) intended for display
        :rtype: List[str]
        """
        if self._term is None:
            term = ""
        else:
            term = self._term.to_string()
        return [self.id, self.error_level, self.category, self.message, term]

    def __repr__(self):
        return f"{self._error_level}: {self._message}"


    @staticmethod
    def get_header_fields():
        return ["ID", "Level", "Category", "Message", "HPO Term"]




class ValidationResultBuilder:
    """
    This class is intended for internal use only, and makes constructing ValidatioResult objects a little easier.
    """

    def __init__(self, phenopacket_id:str):
        self._phenopacket_id = phenopacket_id
        self._error_level = ErrorLevel.UNKNOWN
        self._category = Category.UNKNOWN
        self._message = ""
        self._term = None

    def duplicate_term(self, redundant_term:HpTerm):
        self._error_level = ErrorLevel.WARNING
        self._category = Category.REDUNDANT
        self._message = f"<b>{redundant_term.label}</b> is listed multiple times"
        self._term = redundant_term
        return self

    def redundant_term(self, ancestor_term:HpTerm, descendent_term:HpTerm):
        self._error_level = ErrorLevel.WARNING
        self._category = Category.REDUNDANT
        self._message = f"<b>{ancestor_term.label}</b> is redundant because of <b>{descendent_term.label}</b>"
        self._term = ancestor_term
        return self

    def conflict(self, term:HpTerm, conflicting_term:HpTerm):
        message = f"{term.to_string()} conflicts with the excluded term {conflicting_term.to_string()} "
        self._error_level = ErrorLevel.ERROR
        self._category = Category.CONFLICT
        self._message = message
        self._term = conflicting_term
        return self

    def not_measured(self, term:HpTerm):
        self._error_level = ErrorLevel.INFORMATION
        self._category = Category.NOT_MEASURED
        self._term = term
        self._message = f"{term.hpo_term_and_id} was listed as not measured and will be omitted"
        return self

    def insufficient_hpos(self, min_hpo:int, n_hpo:int):
        self._message = f"Minimum HPO terms required {min_hpo} but only {n_hpo} found"
        self._error_level = ErrorLevel.ERROR
        self._category = Category.INSUFFICIENT_HPOS
        return self

    def incorrect_allele_count(self, allelic_requirement:AllelicRequirement, observed_alleles:int):
        if allelic_requirement == AllelicRequirement.MONO_ALLELIC:
            self._message = f"Expected one allele for monoallelic but got {observed_alleles} alleles"
        elif allelic_requirement == AllelicRequirement.BI_ALLELIC:
            self._message  = f"Expected two alleles for biallelic but got {observed_alleles} alleles"
        else:
            # should never happen
            raise ValueError("attempt to create incorrect_allele_count Error without defined allelic requirement")
        self._error_level = ErrorLevel.ERROR
        self._category = Category.INCORRECT_ALLELE_COUNT
        return self

    def incorrect_variant_count(self,allelic_requirement:AllelicRequirement, n_var:int):
        if allelic_requirement == AllelicRequirement.MONO_ALLELIC:
            self._message = f"Expected one variant for monoallelic but got {n_var} variants"
        elif allelic_requirement == AllelicRequirement.BI_ALLELIC:
            self._message  = f"Expected one or two variants for biallelic but got {n_var} variants"
        else:
            # should never happen
            raise ValueError("attempt to create incorrect_variant_count Error without defined allelic requirement")
        self._error_level = ErrorLevel.ERROR
        self._category = Category.INCORRECT_VARIANT_COUNT
        return self

    def set_message(self, msg):
        self._message = msg
        return self

    def malformed_hpo_id(self, malformed_term:HpTerm):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.MALFORMED_ID
        self._message = f"Malformed term {malformed_term.label} with invalid HPO id {malformed_term.id}"
        return self

    def malformed_hpo_label(self, hpo_label, valid_term:HpTerm):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.MALFORMED_LABEL
        self._message = f"Invalid label '{hpo_label}' found for {valid_term.to_string()}"
        self._term = valid_term
        return self

    def observed_and_included(self, term:HpTerm):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.OBSERVED_AND_EXCLUDED
        self._message = f"Term {term.label} ({term.id}) was annotated to be both observed and excluded."
        self._term = term
        return self

    def set_term(self, term:HpTerm):
        self._term = term
        return self

    def build(self) -> ValidationResult:
        return ValidationResult(phenopacket_id=self._phenopacket_id, message=self._message, errorlevel=self._error_level, category=self._category, term=self._term)




