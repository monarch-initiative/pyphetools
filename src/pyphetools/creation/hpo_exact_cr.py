import re
import typing

import hpotk

from .hp_term import HpTerm
from .hpo_base_cr import HpoBaseConceptRecognizer, ConceptMatch


def get_label_to_id_map(hpo: hpotk.Ontology) -> typing.Mapping[str, str]:
    """
    Create a map from a lower case version of HPO labels to the corresponding HPO id
    only include terms that are descendants of PHENOTYPE_ROOT

    :returns: a map from lower-case HPO term labels to HPO ids
    """
    label_to_id_d = {}
    for term in hpo.terms:
        hpo_id = term.identifier
        if not hpo.graph.is_ancestor_of(hpotk.constants.hpo.base.PHENOTYPIC_ABNORMALITY, hpo_id):
            continue
        label_to_id_d[term.name.lower()] = hpo_id.value
        # Add the labels of the synonyms
        if term.synonyms is not None and len(term.synonyms) > 0:
            for synonym in term.synonyms:
                lc_syn = synonym.name.lower()
                # only take synonyms with length at least 5 to avoid spurious matches
                if len(lc_syn) > 4:
                    label_to_id_d[lc_syn] = hpo_id.value

    return label_to_id_d


def get_id_to_label_map(hpo: hpotk.MinimalOntology) -> typing.Mapping[str, str]:
    """
    :returns: a map from HPO term ids to HPO labels
    :rtype: Dict[str,str]
    """
    id_to_label_d = {}

    for term in hpo.terms:
        id_to_label_d[term.identifier.value] = term.name

    return id_to_label_d


class HpoExactConceptRecognizer(HpoBaseConceptRecognizer):

    @staticmethod
    def from_hpo(hpo: hpotk.Ontology):
        label_to_id = get_label_to_id_map(hpo)
        id_to_primary_label = get_id_to_label_map(hpo)

        return HpoExactConceptRecognizer(
            label_to_id=label_to_id,
            id_to_primary_label=id_to_primary_label,
        )

    def __init__(self, **kwargs):
        super(HpoExactConceptRecognizer, self).__init__(**kwargs)

    def _find_hpo_term_in_lc_chunk(self, lc_chunk) -> typing.List[HpTerm]:
        hits = []
        for lower_case_hp_label, hpo_tid in self._label_to_id.items():
            key = lower_case_hp_label.lower()
            startpos = lc_chunk.find(key)
            endpos = startpos + len(key) - 1
            if startpos < 0:
                continue
            # If we get here, we demand that the match is a complete word
            # This is because otherwise we get some spurious matches such as Pica HP:0011856 matching to typical
            # Create a regex to enforce the match is at word boundary
            BOUNDARY_REGEX = re.compile(r'\b%s\b' % key, re.I)
            if BOUNDARY_REGEX.search(lc_chunk):
                hp_term = super(HpoExactConceptRecognizer, self).get_term_from_id(
                    hpo_id=hpo_tid)  # Get properly capitalized label
                hits.append(ConceptMatch(term=hp_term, start=startpos, end=endpos))
        return hits
