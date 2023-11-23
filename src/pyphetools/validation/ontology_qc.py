import hpotk
from collections import Counter
from typing import List, Optional
from ..creation.hp_term import HpTerm
from .validation_result import ValidationResult, ValidationResultBuilder
from collections import defaultdict
from ..creation.individual import Individual



class OntologyQC:
    """
    This class performs two kind of checks/cleansing of ontology data
    1. negated superclass and observed subclass (this is an error in the original data)
    2. observed superclass and observed subclass (this is a redundancy but arguably not an error)

    """

    def __init__(self, ontology:hpotk.MinimalOntology, individual:Individual, fix_conflicts=True, fix_redundancies=True):
        self._ontology = ontology
        self._individual = individual
        self._phenopacket_id = individual.get_phenopacket_id()
        self._fix_conflict_flag = fix_conflicts
        self._fix_redundancy_flag = fix_redundancies
        self._errors = []
        self._clean_hpo_terms = self._clean_terms()


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
                    error = ValidationResultBuilder(phenopacket_id=self._phenopacket_id).error().conflict().set_term(term=term).build()
                    self._errors.append(error)
        if len(conflicting_term_id_set) > 0:
            excluded_hpo_terms = [term for term in excluded_hpo_terms if term.id not in conflicting_term_id_set]
        return excluded_hpo_terms




    def _fix_redundancies(self, hpo_terms:List[HpTerm]) -> List[HpTerm]:
        """
        Remove redundant terms from a list of HPO terms.

        As a side effect, add a ValidationResult for each removed redundant term
        :param hpo_terms: original term list that might contain redundancies
        :type hpo_terms: List[HpTerm]
        :returns: list of HPO terms without redundancies
        :rtype hpo_terms: List[HpTerm]
        """
        all_terms = set(hpo_terms)
        # check for duplicates
        if len(all_terms) != len(hpo_terms):
            duplicates = [item for item, count in Counter(hpo_terms).items() if count > 1]
            for dup in duplicates:
                message = f"<b>{dup.label}</b> is listed multiple times"
                error = ValidationResultBuilder(self._phenopacket_id).warning().redundant().set_message(
                    message).set_term(dup).build()
                self._errors.append(error)
                hpo_terms.remove(dup)
        # The following code checks for other kinds of redundancies
        redundant_term_d = {}
        for term in all_terms:
            for term2 in all_terms:
                # The ancestor, e.g. Seizure comes first, the other term, e.g. Clonic seizure, second
                # in the following function call
                if self._ontology.graph.is_ancestor_of(term2.id, term.id):
                    redundant_term_d[term2] = term
        # When we get here, we have scanned all terms for redundant ancestors
        non_redundant_terms = [ term for term in hpo_terms if term not in redundant_term_d]
        if len(redundant_term_d) > 0:
            for term, descendant in redundant_term_d.items():
                message = f"<b>{term.label}</b> is redundant because of <b>{descendant.label}</b>"
                error = ValidationResultBuilder(self._phenopacket_id).warning().redundant().set_message(message).set_term(term).build()
                self._errors.append(error)
        return non_redundant_terms


    def _check_terms(self, hpo_terms:List[HpTerm]) -> None:
        for term in hpo_terms:
            hpo_id = term.id
            if not hpo_id in self._ontology:
                error = ValidationResultBuilder(self._phenopacket_id).error().malformed_hpo_id(hpo_id).build()
                self._errors.append(error)
            else:
                hpo_term = self._ontology.get_term(term_id=hpo_id)
                if hpo_term.name != term.label:
                    error = ValidationResultBuilder(self._phenopacket_id).error().malformed_hpo_label(term.label).build()
                    self._errors.append(error)

    def _clean_terms(self) -> List[HpTerm]:
        """
        :returns: list of HPO terms without redundancies/conflicts
        :rtype hpo_terms: List[HpTerm]
        """
        by_age_dictionary =  defaultdict(list)
        for term in self._individual.hpo_terms:
            if not term.measured:
                self._errors.append(ValidationResultBuilder(self._phenopacket_id).not_measured(term=term))
            else:
                by_age_dictionary[term.onset].append(term)
        self._check_terms(self._individual.hpo_terms)
        clean_terms = []
        self._errors.clear() # reset
        for onset, term_list in by_age_dictionary.items():
            observed_hpo_terms = [term for term in term_list if term.observed]
            excluded_hpo_terms = [term for term in term_list if not term.observed]
            if self._fix_redundancy_flag:
                observed_hpo_terms = self._fix_redundancies(observed_hpo_terms)
                excluded_hpo_terms = self._fix_redundancies(excluded_hpo_terms)
            if self._fix_conflict_flag:
                # this method checks and may fix the excluded terms (only)
                excluded_hpo_terms = self._fix_conflicts(observed_hpo_terms, excluded_hpo_terms)
            clean_terms.extend(observed_hpo_terms)
            clean_terms.extend(excluded_hpo_terms)
        return clean_terms

    def has_error(self) -> bool:
        """
        :returns: True iff errors were encountered
        :rtype: boolean
        """
        return len(self._errors) > 0

    def get_error_list(self) -> List[ValidationResult]:
        """
        :returns: a potential empty list of errors
        :rtype: List[str]
        """
        return self._errors

    def get_clean_terms(self) -> List[HpTerm]:
        return self._clean_hpo_terms


    def get_error_string(self) -> Optional[str]:
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


    @staticmethod
    def qc_cohort(individual_list:List[Individual]) -> List[Individual] :


        return individual_list
