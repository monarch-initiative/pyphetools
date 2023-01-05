import re
from typing import List
from collections import defaultdict
from .hp_term import HpTerm
from .hpo_cr import HpoConceptRecognizer



ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"





class CaseParser:
    
    
    def __init__(self, concept_recognizer, pmid, age_at_last_exam=None) -> None:
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._concept_recognizer = concept_recognizer
        if not pmid.startswith("PMID:"):
            raise ValueError(f"Malformed pmid argument ({pmid}). Must start with PMID:")
        self._pmid = pmid
        if age_at_last_exam is not None:
            match = re.search(ISO8601_REGEX, age_at_last_exam)
            if match:
                self._age_at_last_examination = age_at_last_exam
            else:
                raise ValueError(f"Could not parse {age_at_last_exam} as ISO8601 period")
        else:
            self._age_at_last_examination = None

        self._annotations = defaultdict(list)


    def add_vignette(self, vignette, custom_d=None, custom_age=None) -> List[HpTerm]:
        if custom_d is None:
            custom_d = {}
        results =  self._concept_recognizer._parse_chunk(chunk=vignette, custom_d=custom_d)
        if custom_age is not None:
            self._annotations[custom_age].extend(results)
        elif self._age_at_last_examination is not None:
            self._annotations[self._age_at_last_examination].extend(results)
        else:
            self._annotations["N/A"].extend(results)
        return HpTerm.term_list_to_dataframe(results)
        
