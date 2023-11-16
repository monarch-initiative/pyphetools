from enum import Enum
from typing import List, Optional
from ..creation.hp_term import HpTerm


class ErrorLevel(Enum):
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"

class Category(Enum):
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
    UNKNOWN = 8


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
    def error_level(self):
        if self._error_level == ErrorLevel.ERROR:
            return 'error'
        elif self._error_level == ErrorLevel.WARNING:
            return 'warning'
        elif self._error_level == ErrorLevel.UNKNOWN:
            return 'unknown'
        else:
            raise ValueError(f"Did not recognize error level {self._error_level}")

    @property
    def message(self):
        return self._message

    @property
    def error_level(self):
        return self._error_level

    @property
    def term(self):
        return self._term

    @property
    def category(self):
        return self._category

    def get_items_as_array(self):
        if self.term is None:
            term = ""
        else:
            term = self.term.hpo_term_and_id
        return [self._error_level.name, self.category.name, self.message, term]

    def __repr__(self):
        return f"{self._error_level}: {self._message}"


    @staticmethod
    def get_header_fields():
        return ["Level", "Category", "Message", "HPO Term"]




class ValidationResultBuilder:
    """
    This class is intended for internal use only, and makes constructing ValidatioResult objects a little easier.
    """

    def __init__(self, ppkt_id:str):
        self._phenopacket_id = ppkt_id
        self._error_level = ErrorLevel.UNKNOWN
        self._category = Category.UNKNOWN
        self._message = ""
        self._term = None

    def warning(self):
        self._error_level = ErrorLevel.WARNING
        return self

    def error(self):
        self._error_level = ErrorLevel.ERROR
        return self

    def redundant(self):
        self._category = Category.REDUNDANT
        return self

    def conflict(self):
        self._category = Category.CONFLICT
        return self

    def insufficient_hpos(self):
        self._category = Category.INSUFFICIENT_HPOS
        return self

    def incorrect_allele_count(self):
        self._category = Category.INCORRECT_ALLELE_COUNT
        return self

    def incorrect_variant_count(self):
        self._category = Category.INCORRECT_VARIANT_COUNT
        return self

    def set_message(self, msg):
        self._message = msg
        return self

    def malformed_hpo_id(self, hpo_id):
        self._category = Category.MALFORMED_ID
        self._message = f"Invalid HPO id {hpo_id}"

    def malformed_hpo_label(self, hpo_label):
        self._category = Category.MALFORMED_LABEL
        self._message = f"Invalid HPO id {hpo_label}"

    def set_term(self, term:HpTerm):
        self._term = term
        return self


    def build(self) -> ValidationResult:
        return ValidationResult(phenopacket_id=self._phenopacket_id, message=self._message, errorlevel=self._error_level, category=self._category, term=self._term)



