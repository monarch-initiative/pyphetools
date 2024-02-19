from collections import defaultdict
from typing import Dict, List, Optional
from ..creation.constants import Constants
from ..creation.iso_age import IsoAge
from ..creation.hp_term import HpTerm

ONSET_TERMS = {
    # Onset of symptoms after the age of 60 years.
    "Late onset": HpTerm(hpo_id="HP:0003584", label="Late onset"),
    "Middle age onset": HpTerm(hpo_id="HP:0003596",label="Middle age onset"),
    "Young adult onset": HpTerm(hpo_id="HP:0011462", label="Young adult onset"),
    # Onset of disease after 16 years  .
    "Adult onset":  HpTerm(hpo_id="HP:0003581", label="Adult onset"),
    #Onset of signs or symptoms of disease between the age of 5 and 15 years.
    "Juvenile onset": HpTerm(hpo_id="HP:0003621", label="Juvenile onset"),
    #Onset of disease at the age of between 1 and 5 years.
    "Childhood onset": HpTerm(hpo_id="HP:0011463", label="Childhood onset"),
    # Onset of signs or symptoms of disease between 28 days to one year of life.
    "Infantile onset": HpTerm(hpo_id="HP:0003593", label="Infantile onset"),
    # Onset of signs or symptoms of disease within the first 28 days of life.
    "Neonatal onset": HpTerm(hpo_id="HP:0003623", label="Neonatal onset"),
    # A phenotypic abnormality that is present at birth.
    "Congenital onset": HpTerm(hpo_id="HP:0003577", label="Congenital onset"),
    #  onset prior to birth
    "Antenatal onset": HpTerm(hpo_id="HP:0030674", label="Antenatal onset"),
    #Onset of disease at up to 8 weeks following fertilization (corresponding to 10 weeks of gestation).
    "Embryonal onset": HpTerm(hpo_id="HP:0011460", label="Embryonal onset"),
    # Onset prior to birth but after 8 weeks of embryonic development (corresponding to a gestational age of 10 weeks).
    "Fetal onset": HpTerm(hpo_id="HP:0011461", label="Fetal onset"),
    #late first trimester during the early fetal period, which is defined as 11 0/7 to 13 6/7 weeks of gestation (inclusive).
    "Late first trimester onset": HpTerm(hpo_id="HP:0034199", label="Late first trimester onset"),
    # second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive)
    "Second trimester onset": HpTerm(hpo_id="HP:0034198", label="Second trimester onset"),
    #third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
    "Third trimester onset":  HpTerm(hpo_id="HP:0034197", label="Third trimester onset"),
}

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
            if disease.onset is not None and disease.onset.age is not None:
                iso8601age = disease.onset.age.iso8601duration
                onset_term = self.onset_to_hpo_term(iso8601age)
                if onset_term is None or onset_term == Constants.NOT_PROVIDED:
                    continue
                self._pmid_to_onsetlist_d[pmid].append(onset_term)
            elif disease.onset is not None and disease.onset.ontology_class is not None:
                label = disease.onset.ontology_class.label
                onset_term =  self.onset_to_hpo_term(label)
                if onset_term is None or onset_term == Constants.NOT_PROVIDED:
                    continue
                self._pmid_to_onsetlist_d[pmid].append(onset_term)

    def onset_to_hpo_term(self, onset_string) ->Optional[HpTerm]:
        """
        try to retrieve an HPO term that represents the age of onset. This can be either an HPO term such as Antenatal onset
        or an iso8601 string. If nothing can be found (e.g., for "na"), return None
        """
        if onset_string in ONSET_TERMS:
            return ONSET_TERMS.get(onset_string)
        if onset_string is None or onset_string.lower() == "na":
            return None
        iso_age = IsoAge.from_iso8601(onset_string)
        if iso_age.years >= 60:
            return ONSET_TERMS.get("Late onset")
        elif iso_age.years >= 40:
            return  ONSET_TERMS.get("Middle age onset")
        elif iso_age.years >= 16:
            return  ONSET_TERMS.get("Young adult onset")
        elif iso_age.years >= 5:
            return ONSET_TERMS.get("Juvenile onset")
        elif iso_age.years >= 1:
            return ONSET_TERMS.get("Childhood onset")
        elif iso_age.months >= 1:
            return ONSET_TERMS.get("Infantile onset")
        elif iso_age.days >= 1:
            return ONSET_TERMS.get("Neonatal onset")
        elif iso_age.days == 0:
            return ONSET_TERMS.get("Congenital onset")
        # if we get here, we could not find anything. This may be an error, because according to our template,
        # the user must enter an iso8601 string or an HPO label
        raise ValueError(f"Could not identify HPO onset term for {onset_string}")


    def get_pmid_to_onset_d(self)-> Dict[str, List[HpTerm]]:
        return self._pmid_to_onsetlist_d






