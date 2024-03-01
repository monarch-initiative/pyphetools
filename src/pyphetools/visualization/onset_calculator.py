from collections import defaultdict
from typing import Dict, List
import re
from ..creation.pyphetools_age import HPO_ONSET_TERMS
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
                # onset is a GA4GH TimeElement
                # In pyphetools, it can be an OntologyClass, an Age, or a GestationalAge
                onset = disease.onset
                if onset.HasField("ontology_class"):
                        onset_term = onset.ontology_class
                        hpo_onset_term = HpTerm(hpo_id=onset_term.id, label=onset_term.label)
                        self._pmid_to_onsetlist_d[pmid].append(hpo_onset_term)
                elif onset.HasField("age"):
                    hpo_onset_term = self._get_hpo_onset_term_from_iso8601(onset.age.iso8601duration)
                    self._pmid_to_onsetlist_d[pmid].append(hpo_onset_term)
                elif onset.HasField("gestational_age"):
                    hpo_onset_term = self._get_hpo_onset_term_from_gestational_age(onset.age.iso8601duration)
                    self._pmid_to_onsetlist_d[pmid].append(hpo_onset_term)
                else:
                    raise ValueError(f"onset was present but could not be decoded: {onset}")


    def _get_hpo_onset_term_from_iso8601(self, isostring):
        # the following regex gets years, months, days - optionally (when we get to this point in pyphetools, we cannot have weeks)
        ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"
        match = re.search(ISO8601_REGEX, isostring)
        if match:
            y = match.group(1) or "0Y"
            m = match.group(2) or "0M"
            d = match.group(3) or "0D"
            y = int(y[0:-1]) # all but last character
            m = int(m[0:-1])
            d = int(d[0:-1])
            label = None
            if y >= 60:
                label = "Late onset"
            elif y >= 40:
                label = "Middle age onset"
            elif y >= 16:
                label = "Young adult onset"
            elif y >= 5:
                label = "Juvenile onset"
            elif y >= 1:
                label = "Childhood onset"
            elif m >= 1:
                label = "Infantile onset"
            elif d  >= 1:
                label = "Neonatal onset"
            elif d == 0:
                label = "Congenital onset"
            else:
                raise ValueError(f"[ERROR] Could not parse iso8601 \"{isostring}\"")
            if label not in HPO_ONSET_TERMS:
                # should never happen ...
                raise ValueError(f"Could not identify onset label {label}")
            hpo_id = HPO_ONSET_TERMS.get(label)
            return HpTerm(hpo_id=hpo_id, label=label)

    def _get_hpo_onset_term_from_gestational_age(self, gestational_age):
        weeks = gestational_age.weeks
        # days not relevant to identifying the HPO Onset term
        label = None
        if weeks >= 28:
            # prior to birth during the third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
            label = "Third trimester onset" # HP:0034197
        elif weeks >= 14:
            # prior to birth during the second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive).
            label = "Second trimester onset" # HP:0034198
        elif weeks >= 11:
            # 11 0/7 to 13 6/7 weeks of gestation (inclusive).
            label = "Late first trimester onset"  #  HP:0034199
        else:
            label = "Embryonal onset"
        if label not in HPO_ONSET_TERMS:
                # should never happen ...
                raise ValueError(f"Could not identify onset label {label}")
        hpo_id = HPO_ONSET_TERMS.get(label)
        return HpTerm(hpo_id=hpo_id, label=label)


    def get_pmid_to_onset_d(self)-> Dict[str, List[HpTerm]]:
        return self._pmid_to_onsetlist_d






