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

    def get_validated_individual_list(self):
        return self._validated_individual_list