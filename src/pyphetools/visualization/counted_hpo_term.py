from collections import defaultdict


class CountedHpoTerm:
    """
    This class intends to keep track of the frequzency of an HPO term in a cohort
    """
    def __init__(self, hpo_term, numerator, denominator):
        if not isinstance(numerator, int):
            raise ValueError(f"Malformed numerator (must be integer but was {numerator})")
        if not isinstance(denominator, int):
            raise ValueError(f"Malformed denominator (must be integer but was {denominator})")
        self._onset_term_id = hpo_term.id
        self._onset_term_label = hpo_term.label
        self._num = numerator
        self._denom = denominator

    @property
    def id(self):
        return self._onset_term_id

    @property
    def label(self):
        return self._onset_term_label

    def has_frequency(self):
        return self._num is not None and self._denom is not None

    @property
    def numerator(self):
        return self._num

    @property
    def denominator(self):
        return self._denom

    def increment_numerator(self):
        self._num += 1


class CohortTermCounter:

    def __init__(self, pmid):
        self._pmid = pmid
        self._term_to_count_d = defaultdict(int)
        self._total = 0

    def increment_term(self, hpterm):
        self._term_to_count_d[hpterm] += 1
        self._total += 1

    def get_counted_terms(self):
        counted_terms = list()
        for k, v in self._term_to_count_d.items():
            cterm = CountedHpoTerm(hpo_term=k, numerator=v, denominator=self._total)
            counted_terms.append(cterm)
        return counted_terms

    def get_pmid(self):
        return self._pmid

