import hpotk
from typing import List, Optional
from .hp_term import HpTerm
from enum import Enum
from collections import defaultdict

class Category(Enum):
    REDUNDANT = 1
    CONFLICT = 2


class QcError:
    """
    Data class for quality control errors. Should not be used by client code.

    :param category: type of QcError
    :type category: Category
    :param term: HpTerm that caused the error
    :type term: HpTerm
    """
    def __init__(self, category:Category, term:HpTerm):
        if not isinstance(term, HpTerm):
            raise ValueError(f"\"term\" argument must be HpTerm but was {type(term)}")
        self._category = category
        self._term = term

    def is_redundant(self):
        return Category.REDUNDANT == self._category

    def is_conflict(self):
        return Category.CONFLICT == self._category

    @property
    def category(self):
        return self._category

    @property
    def term(self):
        return self._term

    def get_summary(self):
        """
        :returns: A summary of the error, intended to show in the notebook
        :rtype: str
        """
        return f"{self._category}: {self._term.label} ({self._term.id})"


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
        This class detects excluded superclasses that have observed subclasses -- a conflict.

        For instance, if an individual is annotated to the terms (1) excluded: Seizure [HP:0001250] and (2)
        observed - Clonic Seizure [HP:0020221], this is a conflict, because a person with clonic seizure also
        can be said to have seizure. Here, we assume that the excluded annotation is an error that we
        want to remove automatically and issue a warning. Thus, in this example, we would remove the
        annotation excluded: Seizure [HP:0001250], and in general the excluded superclass is removed
        if this kind of conflict is detected

        :param observed_hpo_terms: list of HPO terms (observed), can be empty
        :type observed_hpo_terms: List[HpTerm]
        :param excluded_hpo_terms: list of HPO terms (excluded), can be empty
        :type excluded_hpo_terms: List[HpTerm]
        :returns: the potentially cleansed list of excluded terms (the observed terms are never changed by this method
        :rtype: List[HpTerm]
        """
        if len(excluded_hpo_terms) == 0:
            # i.e., there can be no conflict
            return excluded_hpo_terms
        all_excluded_term_ids = {term.id for term in excluded_hpo_terms}
        conflicting_term_id_set = set()
        for term in observed_hpo_terms:
            for tid in all_excluded_term_ids:
                if self._ontology.graph.is_ancestor_of(tid, term.id):
                    conflicting_term_id_set.add(tid)
        if len(conflicting_term_id_set) > 0:
            excluded_hpo_terms = [term for term in excluded_hpo_terms if term.id not in conflicting_term_id_set]
        return excluded_hpo_terms




    def _fix_redundancies(self, hpo_terms:List[HpTerm]) -> List[HpTerm]:
        """
        Remove redundant terms from a list of HPO terms.

        As a side effect, add a QcError for each removed redundant term
        :param hpo_terms: original term list that might contain redundancies
        :type hpo_terms: List[HpTerm]
        :returns: list of HPO terms without redundancies
        :rtype hpo_terms: List[HpTerm]
        """
        all_terms = set(hpo_terms)
        redundant_term_set = set()
        for term in all_terms:
            for term2 in all_terms:
                # The ancestor, e.g. Seizure comes first, the other term, e.g. Clonic seizure, second
                # in the following function call
                if self._ontology.graph.is_ancestor_of(term2.id, term.id):
                    redundant_term_set.add(term2)
        # When we get here, we have scanned all terms for redundant ancestors
        non_redundant_terms = [ term for term in hpo_terms if term not in redundant_term_set]
        if len(redundant_term_set) > 0:
            for term in redundant_term_set:
                error = QcError(Category.REDUNDANT, term)
                self._errors.append(error)
        return non_redundant_terms



    def clean_terms(self, hpo_terms:List[HpTerm], fix_conflicts=True, fix_redundancies=True) -> List[HpTerm]:
        """
        :param hpo_terms: original term list that might contain redundancies or conflicts
        :type hpo_terms: List[HpTerm]
        :returns: list of HPO terms without redundancies/conflicts
        :rtype hpo_terms: List[HpTerm]
        """
        by_age_dictionary =  defaultdict(list)
        for term in hpo_terms:
            by_age_dictionary[term.onset].append(term)
        clean_terms = []
        self._errors.clear() # reset
        for onset, term_list in by_age_dictionary.items():
            observed_hpo_terms = [term for term in term_list if term.observed]
            excluded_hpo_terms = [term for term in term_list if not term.observed]
            if fix_redundancies:
                observed_hpo_terms = self._fix_redundancies(observed_hpo_terms)
                excluded_hpo_terms = self._fix_redundancies(excluded_hpo_terms)
            if fix_conflicts:
                # this method checks and may fix the excluded terms (only)
                excluded_hpo_terms = self._fix_conflicts(observed_hpo_terms, excluded_hpo_terms)
            clean_terms.extend(observed_hpo_terms)
            clean_terms.extend(excluded_hpo_terms)
        return clean_terms

    def has_error(self):
        """
        :returns: True iff errors were encountered
        :rtype: boolean
        """
        return len(self._errors) > 0

    def get_error_list(self):
        """
        :returns: a potential empty list of errors
        :rtype: List[str]
        """
        return [x.get_summary() for x in self._errors]


    def get_error_string(self):
        """
        create and return a string that summarizes the redundancies and conflicts that were corrected

        :returns: a string summarizing errors or None if there were none
        :rtype: Optional[str]
        """
        if not self.has_error():
            return None
        redundancies = [e for e in self._errors if e.is_redundant()]
        conflicts = [e for e in self._errors if e.is_conflict()]
        e_string = ""
        if len(redundancies) > 0:
            red_terms = [e.hpo_term_and_id for e in redundancies]
            e_string = "The following redundant terms were removed: " + ", ".join(red_terms) + ". "
        if len(conflicts) > 0:
            conf_terms = [e.hpo_term_and_id for e in conflicts]
            e_string = e_string + "The following conflicting excluded terms were removed: " + ", ".join(conf_terms) + ". "
        return e_string
