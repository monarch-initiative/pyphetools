import hpotk
from typing import List
from .hp_term import HpTerm


class OntologyQC:
    """
    This class performs two kind of checks/cleansing of ontology data
    1. negated superclass and observed subclass (this is an error in the original data)
    2. observed superclass and observed subclass (this is a redundancy but arguably not an error)

    """

    def __int__(self, ontology:hpotk.MinimalOntology):
        self._ontology = ontology


    def _fix_conflicts(self, hpo_terms:List[HpTerm]) -> List[List[HpTerm], str]:
        """
        :param hpo_terms:list of HPO terms, potentially observed and excluded
        :type hpo_terms:List[HpTerm]
        """


    def clean_terms(self, hpo_terms:List[HpTerm], fix_conflicts=True, fix_redundancies=True) -> List[List[HpTerm], str]:
        pass


