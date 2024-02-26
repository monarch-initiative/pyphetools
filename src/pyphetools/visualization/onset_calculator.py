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
            if disease.onset is not None and disease.onset is not None:
                onset_term = self.onset_to_hpo_term(disease.onset)
                if onset_term is None or onset_term == Constants.NOT_PROVIDED:
                    continue
                self._pmid_to_onsetlist_d[pmid].append(onset_term)
            elif disease.onset is not None and disease.onset.ontology_class is not None:
                label = disease.onset.ontology_class.label
                onset_term =  self.onset_to_hpo_term(label)
                if onset_term is None or onset_term == Constants.NOT_PROVIDED:
                    continue
                self._pmid_to_onsetlist_d[pmid].append(onset_term)

    def onset_to_hpo_term(self, onset:Union[PyPheToolsAge, str]) ->Optional[HpTerm]:
        """
        try to retrieve an HPO term that represents the age of onset. This can be either an HPO term such as Antenatal onset
        or an iso8601 string. If nothing can be found (e.g., for "na"), return None
        """
        if isinstance(onset, PyPheToolsAge):
            onset_string = onset.age_string
        elif isinstance(onset, str):
            onset_string = onset
        else:
            return None
        return PyPheToolsAge.onset_to_hpo_term(onset_string=onset_string)

    def get_pmid_to_onset_d(self)-> Dict[str, List[HpTerm]]:
        return self._pmid_to_onsetlist_d






