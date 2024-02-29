from collections import defaultdict
from typing import Dict, List, Optional, Union
from ..creation.constants import Constants
from ..creation.pyphetools_age import PyPheToolsAge
from ..creation.hp_term import HpTerm


class OnsetCalculator:
    """
    This class calculates the age of onset anntoations for the HPOA file
    """
    def __init__(self, phenopacket_list):
        if not isinstance(phenopacket_list, list):
            raise ValueError(f"Malformed individual_list argument -- needs to be list but was {type(phenopacket_list)} ")
        self._pmid_to_onsetlist_d = defaultdict(list)
        for ppack in phenopacket_list:
            mdata = ppack.meta_data
            pmid = None
            if len(mdata.external_references) == 1:
                eref = mdata.external_references[0]
                pmid = eref.id
            else:
                print("Warning: Could not identify pmid")
            if len(ppack.diseases) == 0:
                print("Warning: Could not identify disease element")
            elif len(ppack.diseases) > 1:
                print("Warning: Identified multiple disease element")
            disease = ppack.diseases[0]
            if disease.HasField("onset"):
                onset = disease.onset
                if onset.HasField("ontology_class"):
                    onset_term = onset.ontology_class
                    hpo_onset_term = HpTerm(hpo_id=onset_term.id, label=onset_term.label)
                    self._pmid_to_onsetlist_d[pmid].append(hpo_onset_term)
                elif  onset.HasField("age"):
                    isoage = onset.age.iso8601duration
                    hpo_onset_term = PyPheToolsAge.onset_to_hpo_term(onset_string=isoage)
                    if hpo_onset_term is not None and hpo_onset_term != Constants.NOT_PROVIDED:
                        self._pmid_to_onsetlist_d[pmid].append(hpo_onset_term)
                else:
                    print("[ERROR] Could not parse disease onset")
                    print(disease.onset)
                    raise ValueError(f"Could not parse disease onset {disease}")

    def get_pmid_to_onset_d(self)-> Dict[str, List[HpTerm]]:
        return self._pmid_to_onsetlist_d






