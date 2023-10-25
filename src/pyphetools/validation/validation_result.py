from enum import Enum


class ErrorLevel(Enum):
    WARNING = 1
    ERROR = 2


class ValidationResult:
    """
    A helper class to store the results of validation
    :param phenopacket_id: Identifier of the phenopacket being validated
    :type phenopacket_id: str
    :param message: description of the error/warning
    :type message: str
    :param errorlevel: whether this result is an error or a warning
    :type errorlevel: ErrorLevel
    """
    def __init__(self, phenopacket_id:str, message:str, errorlevel:ErrorLevel):
        self._phenopacket_id = phenopacket_id
        self._message = message
        self._error_level = errorlevel

    @property
    def error_level(self):
        if self._error_level == ErrorLevel.ERROR:
            return 'error'
        elif self._error_level == ErrorLevel.WARNING:
            return 'warning'
        else:
            raise ValueError(f"Did not recognize error level {self._error_level}")

    @property
    def message(self):
        return self._message

    @property
    def error_level(self):
        return self._error_level


    @staticmethod
    def error(phenopacket_id:str, message:str):
        return ValidationResult(phenopacket_id=phenopacket_id, message=message, errorlevel=ErrorLevel.ERROR)

    @staticmethod
    def warning(phenopacket_id:str, message:str):
        return ValidationResult(phenopacket_id=phenopacket_id, message=message, errorlevel=ErrorLevel.WARNING)

    def __repr__(self):
        return f"{self._error_level}: {self._message}"




