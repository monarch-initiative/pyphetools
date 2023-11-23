from enum import IntEnum
from typing import List, Optional

from ..creation.hp_term import HpTerm


class ErrorLevel(IntEnum):
    WARNING = 1
    ERROR = 2
    UNKNOWN = 3



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
    def id(self):
        return self._phenopacket_id

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

    def get_items_as_array(self) -> List[str]:
        """
        :returns: A list of items (strings) intended for display
        :rtype: List[str]
        """
        if self._term is None:
            term = term
        else:
            term = term.to_string()
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

    def warning(self):
        self._error_level = ErrorLevel.WARNING
        return self

    def error(self):
        self._error_level = ErrorLevel.ERROR
        return self

    def redundant(self):
        self._error_level = ErrorLevel.WARNING
        self._category = Category.REDUNDANT
        return self

    def conflict(self):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.CONFLICT
        return self

    def insufficient_hpos(self):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.INSUFFICIENT_HPOS
        return self

    def incorrect_allele_count(self):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.INCORRECT_ALLELE_COUNT
        return self

    def incorrect_variant_count(self):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.INCORRECT_VARIANT_COUNT
        return self

    def set_message(self, msg):
        self._message = msg
        return self

    def malformed_hpo_id(self, hpo_id):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.MALFORMED_ID
        self._message = f"Invalid HPO id {hpo_id}"
        return self

    def malformed_hpo_label(self, hpo_label):
        self._error_level = ErrorLevel.ERROR
        self._category = Category.MALFORMED_LABEL
        self._message = f"Invalid HPO id {hpo_label}"
        return self

    def set_term(self, term:HpTerm):
        self._term = term
        return self

    def build(self) -> ValidationResult:
        return ValidationResult(phenopacket_id=self._phenopacket_id, message=self._message, errorlevel=self._error_level, category=self._category, term=self._term)




