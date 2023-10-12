import hpotk
from typing import List
from .hp_term import HpTerm
from enum import Enum

class Category(Enum):
    REDUNDANT = 1
    CONFLICT = 2


class QcError:
    def __init__(self, category:Category, term:HpTerm):
        self._category = category
        self._term = term

    def report(self):
        pass


class OntologyQC:
    """
    This class performs two kind of checks/cleansing of ontology data
    1. negated superclass and observed subclass (this is an error in the original data)
    2. observed superclass and observed subclass (this is a redundancy but arguably not an error)

    """

    def __init__(self, ontology:hpotk.MinimalOntology):
        self._ontology = ontology
        self._errors = []


    def _fix_conflicts(self, observed_hpo_terms:List[HpTerm], excluded_hpo_terms) -> List[HpTerm]:
        """
        This class detects excluded superclasses that have observed subclasses -- a conflict

        If conflicts are detected, the offending superclass is removed.

        :param observed_hpo_terms:list of HPO terms (observed), can be empty
        :type observed_hpo_terms:List[HpTerm]
        :param excluded_hpo_terms:list of HPO terms (excluded), can be empty
        :type excluded_hpo_terms:List[HpTerm]
        """
        if len(excluded_hpo_terms) == 0:
            # i.e., there can be no conflict
            return observed_hpo_terms
        all_excluded_term_ids = {term.id for term in excluded_hpo_terms}
        conflicting_term_id_set = set()
        for term in observed_hpo_terms:
            for tid in all_excluded_term_ids:
                if self._ontology.graph.is_ancestor_of(term.id, tid):
                    conflicting_term_id_set.add(tid)
        if len(conflicting_term_id_set) > 0:
            excluded_hpo_terms = [term for term in excluded_hpo_terms if term.id not in conflicting_term_id_set]
        observed_hpo_terms.extend(excluded_hpo_terms)
        return observed_hpo_terms




    def _fix_redundancies(self, hpo_terms:List[HpTerm]) -> List[HpTerm]:
        all_terms = set(hpo_terms)
        all_term_ids = {term.id for term in hpo_terms}
        redundant_term_id_set = set()
        for term in all_terms:
            for tid in all_term_ids:
                if self._ontology.graph.is_ancestor_of(term.id, tid):
                    redundant_term_id_set.add(tid)
        # When we get here, we have scanned all terms for redundant ancestors
        non_redundant_terms = [ term for term in hpo_terms if term.id not in redundant_term_id_set]
        if len(redundant_term_id_set) > 0:
            for tid in redundant_term_id_set:
                error = QcError(Category.REDUNDANT, tid)
                self._errors.append(error)
        return non_redundant_terms



    def clean_terms(self, hpo_terms:List[HpTerm], fix_conflicts=True, fix_redundancies=True) -> List[HpTerm]:
        observed_hpo_terms = [term for term in hpo_terms if term.observed]
        excluded_hpo_terms = [term for term in hpo_terms if not term.observed]
        self._errors = []
        if fix_redundancies:
            observed_hpo_terms = self._fix_redundancies(observed_hpo_terms)
            excluded_hpo_terms = self._fix_redundancies(excluded_hpo_terms)
        if fix_conflicts:
            hpo_terms, conflict_report = self._fix_conflicts(observed_hpo_terms, excluded_hpo_terms)
        return hpo_terms

    def has_error(self):
        return len(self._errors) > 0


