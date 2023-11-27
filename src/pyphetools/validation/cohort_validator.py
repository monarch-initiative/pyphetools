from typing import List
from ..creation.allelic_requirement import AllelicRequirement
from ..creation.individual import Individual
from .validated_individual import ValidatedIndividual
import hpotk

class CohortValidator:

    def __init__(self, cohort:List[Individual], ontology:hpotk.MinimalOntology, min_hpo:int,  allelic_requirement:AllelicRequirement=None) -> None:
        self._cohort = cohort
        self._validated_individual_list = []
        for indi in cohort:
            vindi = ValidatedIndividual(individual=indi)
            vindi.validate(ontology=ontology, min_hpo=min_hpo, allelic_requirement=allelic_requirement)
            self._validated_individual_list.append(vindi)
        if len(cohort) != len(self._validated_individual_list):
            # should never happen
            raise ValueError(f"Invalid validation: size of cohort ={len(cohort)} but size of validated individual = {len(self._validated_individual_list)}")
        self._error_free_individuals = [vi.get_individual_with_clean_terms() for vi in self._validated_individual_list if not vi.has_unfixed_error()]
        self._v_individuals_with_unfixable_errors = [vi for vi in self._validated_individual_list if vi.has_unfixed_error()]

    def get_validated_individual_list(self):
        """
        :returns: list of all individuals with QC Validation results
        :rtype: List[ValidatedIndividual]
        """
        return self._validated_individual_list


    def get_error_free_individual_list(self) -> List[Individual]:
        """
        Returns a list of individuals from which the erroneous and redundant termas have been removed and from which individuals with errors (e.g., not enough HPO terms) have been removed.
        :returns: List of individuals with no errors
        :rtype: List[Individual]
        """
        return self._error_free_individuals

    def get_validated_individuals_with_unfixable_errors(self):
        """
        Returns a list of individuals with errors that cannot be automatically fixed.
        :returns: List of individuals with unfixable errors
        :rtype: List[ValidatedIndivudal]
        """
        return self._v_individuals_with_unfixable_errors


    def n_removed_individuals(self):
        return len(self._validated_individual_list) - len(self._error_free_individuals)

    def n_individuals(self):
        return len(self._validated_individual_list)

    def n_error_free_individuals(self):
        return len(self._error_free_individuals)
