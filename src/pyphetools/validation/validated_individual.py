from ..creation.allelic_requirement import AllelicRequirement
from ..creation.individual import Individual
from .content_validator import ContentValidator
from typing import List
from .validation_result import ValidationResult
from .ontology_qc import OntologyQC
import hpotk

class ValidatedIndividual:

    def __init__(self, individual:Individual) -> None:
        self._individual = individual
        self._clean_terms = []
        self._validation_errors = []

    def validate(self, ontology:hpotk.MinimalOntology, min_hpo:int, allelic_requirement:AllelicRequirement=None) -> None:
        """validate an Individual object for errors in the Ontology or the minimum number of HPO terms/alleles/variants

        :param ontology: HPO object
        :type ontology: hpotk.MinimalOntology
        :param min_hpo: minimum number of phenotypic features (HP terms) for this phenopacket to be considered valid
        :type min_hpo: int
        :param allelic_requirement: used to check number of alleles and variants
        :type allelic_requirement: AllelicRequirement
        """
        cvalidator = ContentValidator(min_hpo=min_hpo, allelic_requirement=allelic_requirement)
        validation_results = cvalidator.validate_individual(individual=self._individual)
        self._validation_errors.extend(validation_results)
        qc = OntologyQC(individual=self._individual, ontology=ontology)
        qc_validation_results = qc.get_error_list()
        self._validation_errors.extend(qc_validation_results)
        self._clean_terms = qc.get_clean_terms()

    def get_individual_with_clean_terms(self) -> Individual:
        """
        :returns: The Individual object input to the class from which redundant/conflicting terms have been removed
        :rtype: Individual
        """
        indi = self._individual
        indi.set_hpo_terms(self._clean_terms)
        return indi

    def get_validation_errors(self) -> List[ValidationResult]:
        return self._validation_errors

    def has_error(self) -> bool:
        """
        :returns: True iff this Individual had oneor more errors
        :rtype: bool
        """
        return len(self._validation_errors) > 0
