import typing

from FastHPOCR.HPOAnnotator import HPOAnnotator

from .hp_term import HpTerm
from .hpo_base_cr import HpoBaseConceptRecognizer, ConceptMatch


class HpoFastHPOCRConceptRecognizer(HpoBaseConceptRecognizer):
    hpoAnnotator = None

    def __init__(self, hp_cr_index: str = None, **kwargs):
        super(HpoFastHPOCRConceptRecognizer, self).__init__(**kwargs)
        self.hpoAnnotator = HPOAnnotator(hp_cr_index)

    def _find_hpo_term_in_lc_chunk(self, lc_chunk) -> typing.List[HpTerm]:
        hits = []
        annotations = self.hpoAnnotator.annotate(lc_chunk)
        for annot in annotations:
            hp_term = super(HpoFastHPOCRConceptRecognizer, self).get_term_from_id(hpo_id=annot.hpoUri)
            hits.append(ConceptMatch(term=hp_term, start=annot.startOffset, end=annot.endOffset))
        return hits
