from enum import Enum


class ErrorLevel(Enum):
    WARNING = 1
    ERROR = 2
    
    
class ValidationResult:
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
    
    
    @staticmethod
    def error(phenopacket_id:str, message:str):
        return ValidationResult(phenopacket_id=phenopacket_id, message=message, errorlevel=ErrorLevel.ERROR)
    
    @staticmethod
    def warning(phenopacket_id:str, message:str):
        return ValidationResult(phenopacket_id=phenopacket_id, message=message, errorlevel=ErrorLevel.WARNING)
        
    
        
        
        
        
     