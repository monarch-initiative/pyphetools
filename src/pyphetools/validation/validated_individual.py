
from ..creation.individual import Individual
from .content_validator import ContentValidator
from typing import List
from .validation_result import ValidationResult


class ValidatedIndividual:

    def __init__(self, individual:Individual) -> None:
        self._individual = individual








    def validate_phenopacket_list(self, individual_list,min_var:int, min_hpo:int, min_allele:int=None) -> List[ValidatedIndividual]:
        """individual_list can be a list of individuals

        :param phenopacket_list: list of GA4GH phenopackets to be validated
        :type phenopacket_list: Union[List[phenopackets.Phenopackets], List[str]]
        :returns: potentially empty list of warnings and errors
        :rtype: List[ValidationResult]
        """
        validated_individual_list = []
        for individual in individual_list:
            cvalidator = ContentValidator(min_hpo=min_hpo, min_allele=min_allele, min_var=min_var)
            validation_results = cvalidator.validate_individual(individual=individual)

            validation_results.extend(self.validate_phenopacket(pp))
        return validation_results