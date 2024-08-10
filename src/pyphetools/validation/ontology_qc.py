import hpotk
from collections import Counter
from typing import List, Optional
from ..creation.hp_term import HpTerm
from .validation_result import ValidationResult, ValidationResultBuilder
from collections import defaultdict
from ..creation.individual import Individual



class OntologyQC:
    """
    This class performs three kind of checks/cleansing of ontology data
    1. negated superclass and observed subclass (this is an error in the original data)
    2. observed superclass and observed subclass (this is a redundancy but arguably not an error)
    3. Same term is excluded and observed (this is an unfixable error in the original data)

    """

    def __init__(self,
                 ontology:hpotk.MinimalOntology,
                 individual:Individual,
                 fix_conflicts=True,
                 fix_redundancies=True):
        self._ontology = ontology
        self._individual = individual
        self._phenopacket_id = individual.get_phenopacket_id()
        self._fix_conflict_flag = fix_conflicts
        self._fix_redundancy_flag = fix_redundancies
        self._errors = []
        self._clean_hpo_terms = self._clean_terms()


    def _fix_conflicts(self,
                       observed_hpo_terms:List[HpTerm],
                       excluded_hpo_terms) -> List[HpTerm]:
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
                if term.id == tid:
                    # same term observed and excluded
                    # we cannot automatically fix this error
                    # this will be reported and the user will need to check the input data
                    error = ValidationResultBuilder(phenopacket_id=self._phenopacket_id).observed_and_excluded_term(term=term).build()
                    self._errors.append(error)
                elif self._ontology.graph.is_ancestor_of(tid, term.id):
                    conflicting_term_id_set.add(tid)
                    conflicting_term = self._ontology.get_term(term_id=tid)
                    cterm = HpTerm.from_hpo_tk_term(conflicting_term)
                    error = ValidationResultBuilder(phenopacket_id=self._phenopacket_id).conflict(term=term, conflicting_term=cterm).build()
                    self._errors.append(error)
        if len(conflicting_term_id_set) > 0:
            excluded_hpo_terms = [term for term in excluded_hpo_terms if term.id not in conflicting_term_id_set]
        return excluded_hpo_terms




    def _fix_redundancies(self,
                          hpo_terms:List[HpTerm]) -> List[HpTerm]:
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
                error = ValidationResultBuilder(self._phenopacket_id).duplicate_term(redundant_term=dup).build()
                self._errors.append(error)
            # The following removes duplicates under the assumption that all components of the HpTerm are equal
            hpo_terms = set(hpo_terms)
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
                error = ValidationResultBuilder(self._phenopacket_id).redundant_term(ancestor_term=term, descendent_term=descendant).build()
                self._errors.append(error)
        return non_redundant_terms


    def _check_term_ids_and_labels(self,
                                   hpo_terms:List[HpTerm]) -> None:
        """
        Check whether the term identifiers (e.g., HP:0001234) are present in the ontology as primary ids and whether
        the label matches the current priumary label; if not, flag the errors in self._errors
        """
        for term in hpo_terms:
            hpo_id = term.id
            if not hpo_id in self._ontology:
                error = ValidationResultBuilder(self._phenopacket_id).malformed_hpo_id(malformed_term=term).build()
                self._errors.append(error)
            else:
                hpo_term = self._ontology.get_term(term_id=hpo_id)
                if hpo_term.name != term.label:
                    valid_term = HpTerm.from_hpo_tk_term(hpo_term)
                    error = ValidationResultBuilder(self._phenopacket_id).malformed_hpo_label(malformed_label=term.label,
                                                                                              valid_term=hpo_term).build()
                    self._errors.append(error)

    def _clean_terms(self) -> List[HpTerm]:
        """
        :returns: list of HPO terms without redundancies/conflicts
        :rtype hpo_terms: List[HpTerm]
        """
        by_age_dictionary = defaultdict(list)
        # collect all terms without a defined age of onset
        # We will assume these terms exist at all specific ages of onset, thus we need this to calculate redundancy
        observed_terms_without_onset = list()
        excluded_terms_without_onset = list()
        for term in self._individual.hpo_terms:
            if not term.measured:
                self._errors.append(ValidationResultBuilder(self._phenopacket_id).not_measured(term=term).build())
            else:
                if term.onset is not None:
                    by_age_dictionary[term.onset].append(term)
                else:
                    if term.observed:
                        observed_terms_without_onset.append(term)
                    else:
                        excluded_terms_without_onset.append(term)
        self._check_term_ids_and_labels(self._individual.hpo_terms)
        clean_terms = []

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
        # When we get here, clean terms contains terms with specific onsets and conflicting/redundant terms
        # have been removed. There may be terms with no specific onset. We only add such terms if they are neither
        # ancestors or descendants of the specific terms
        observed_terms_without_onset = self._fix_redundancies(observed_terms_without_onset)
        excluded_terms_without_onset = self._fix_redundancies(excluded_terms_without_onset)
        all_term_set = set(clean_terms)
        for t in observed_terms_without_onset:
            addT = True
            for s in all_term_set:
                # keep the term with the age of onset regardless of whether it is more or less specific
                if s.id == t.id:
                    error = ValidationResultBuilder(self._phenopacket_id).duplicate_term(s).build()
                    self._errors.append(error)
                    addT = False
                    break
                if self._ontology.graph.is_ancestor_of(t.id, s.id):
                    error = ValidationResultBuilder(self._phenopacket_id).redundant_term(t, s).build()
                    self._errors.append(error)
                    addT = False
                    break
                if self._ontology.graph.is_ancestor_of(s.id, t.id):
                    error = ValidationResultBuilder(self._phenopacket_id).redundant_term(s, t).build()
                    self._errors.append(error)
                    addT = False
                    break
            if addT:
                clean_terms.append(t)
                all_term_set.add(t)
        # now check for problems with excluded terms
        for t in excluded_terms_without_onset:
            addT = True
            for s in all_term_set:
                # if an excluded term is equal to or ancestor of an observed term this is an error
                if s.id == t.id:
                    error = ValidationResultBuilder(self._phenopacket_id).observed_and_excluded_term(term=s).build()
                    self._errors.append(error)
                    addT = False
                elif self._ontology.graph.is_ancestor_of(t.id, s.id):
                    error = ValidationResultBuilder(self._phenopacket_id).conflict(term=s, conflicting_term=t).build()
                    self._errors.append(error)
                    addT = False
                    break
            if addT:
                clean_terms.append(t)
                all_term_set.add(t)

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
