import os
import json

from google.protobuf.json_format import Parse

from ..creation.disease import Disease
from ..creation.hp_term import HpTerm

EMPTY_CELL = ""

import phenopackets as PPKt
from collections import defaultdict
import pandas as pd

class HpoaTableRow:
    def __init__(self, disease:Disease, hpo_term:HpTerm, publication, biocurator,  freq_num:int=None, freq_denom:int=None):
        self._disease_id = disease.id
        self._disease_label = disease.label
        self._phenotype_id = hpo_term.id
        self._phenotype_name = hpo_term.label
        self._publication = publication
        self._biocuration = biocurator
        if freq_num is not None and freq_denom is not None:
            self._frequency = f"{freq_num}/{freq_denom}"
        else:
            self._frequency = None

    def get_dict(self):
        if self._frequency is not None:
            frequency = self._frequency
        else:
            frequency = EMPTY_CELL
        d = {"#diseaseID": self._disease_id,
            "diseaseName": self._disease_label,
            "phenotypeID": self._phenotype_id,
            "phenotypeName": self._phenotype_name,
            "onsetID":EMPTY_CELL,
            "onsetName": EMPTY_CELL,
            "frequency": frequency,
            "sex": EMPTY_CELL,
            "negation" : EMPTY_CELL,
            "modifier": EMPTY_CELL,
            "description": EMPTY_CELL,
            "publication": self._publication,
            "evidence": "PCS",
            "biocuration": self._biocuration
            }
        return d


class OnsetTerm:
    def __init__(self, onset_term_id, onset_term_label, numerator, denominator):
        self._onset_term_id = onset_term_id
        self._onset_term_label = onset_term_label
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


class HpoaTableCreator:
    """
    Create an HPO "small file" with the following fourteen columns
    1. #diseaseID
    2. diseaseName
    3. phenotypeID
    4. phenotypeName
    5. onsetID
    6. onsetName
    7. frequency
    8. sex
    9. negation
    10. modifier
    11. description
    12. publication
    13. evidence
    14. biocuration
    These should be tab separated fields.

    """
    def __init__(self, phenopacket_list, onset_term_list) -> None:
        self._phenopackets = phenopacket_list
        self._onset_term_list = onset_term_list
        self._all_hpos = set()
        self._get_all_hpos()
        self._pmid = self._get_pmid()
        self._disease = self._get_disease()
        observed, measured = self._count_hpos()
        self._observed_hpos = observed
        self._measured_hpos = measured
        self._biocurator = self._get_biocurator()

    def _get_all_hpos(self):
        for ppkt in self._phenopackets:
            for pf in ppkt.phenotypic_features:
                hpterm = HpTerm(hpo_id=pf.type.id, label=pf.type.label)
                self._all_hpos.add(hpterm)
        print(f"We found a total of {len(self._all_hpos)} HPO terms")

    def _get_pmid(self):
        """
        Check that each phenopacket has the same PMID
        """
        pmid_set = set()
        for ppkt in self._phenopackets:
            mdata = ppkt.meta_data
            if mdata.external_references is None:
                raise ValueError("MetaData must have external_references element for HPOA conversion")
            eref_list = mdata.external_references
            if len(eref_list) != 1:
                raise ValueError(f"MetaData must have exactly one external_references element for HPOA conversion but had {len(eref_list)}")
            eref = eref_list[0]
            pmid_set.add(eref.id)
        if len(pmid_set) == 0:
            raise ValueError("Could not retrieve PMIDs for cohort")
        elif len(pmid_set) > 1:
            pmids = ";".join(pmid_set)
            raise ValueError(f"Error: must have only a single PMID for HPOA conversion but we found {pmids}")
        [pmid] = pmid_set
        print(f"extracted PubMed identifier: {pmid}")
        return pmid

    def _get_disease(self):
        disease_set = set()
        for ppkt in self._phenopackets:
            interpretations = ppkt.interpretations
            if len(interpretations) != 1:
                raise ValueError(f"Error: must have only a single disease for HPOA conversion but we found {len(interpretations)}")
            interpretation = interpretations[0]
            if interpretation.diagnosis is None:
                raise ValueError(f"Could not get diagnosis object from interpretation with id {interpretation.id}")
            diagnosis = interpretation.diagnosis
            disease = Disease(disease_id=diagnosis.disease.id, disease_label=diagnosis.disease.label)
            disease_set.add(disease)
        if len(disease_set) == 0:
            raise ValueError("Could not retrieve Disease for cohort")
        elif len(disease_set) > 1:
            raise ValueError(f"Error: must have only a single Disease for HPOA conversion but we found {len(disease_set)}")
        [disease] = disease_set
        print(f"Extracted disease: {disease}")
        return disease

    def _get_biocurator(self):
        biocurator_set = set()
        for ppkt in self._phenopackets:
            mdata = ppkt.meta_data
            created_by = mdata.created_by
            biocurator_set.add(created_by)
        if len(biocurator_set) != 1:
            raise ValueError(f"Currently this script supports only one biocurator per cohort")
        [biocurator] = biocurator_set
        return biocurator

    def _count_hpos(self):
        observed = defaultdict(int)
        measured = defaultdict(int)
        for ppkt in self._phenopackets:
            for pf in ppkt.phenotypic_features:
                hpterm = HpTerm(hpo_id=pf.type.id, label=pf.type.label)
                measured[hpterm.id] += 1
                if pf.excluded is not None and not pf.excluded:
                    observed[hpterm.id] += 1
        return observed, measured

    def get_dataframe(self):
        rows = []
        column_names = ["#diseaseID", "diseaseName", "phenotypeID", "phenotypeName", "onsetID",
                        "onsetName", "frequency", "sex", "negation",  "modifier",
                        "description", "publication","evidence", "biocuration"]
        for hpo in self._all_hpos:
            n = self._observed_hpos.get(hpo.id)
            m = self._measured_hpos.get(hpo.id)
            row = HpoaTableRow(disease=self._disease, hpo_term=hpo, publication=self._pmid, biocurator=self._biocurator, freq_num=n, freq_denom=m)
            rows.append(row.get_dict())
        for oterm in self._onset_term_list:
            hpterm = HpTerm(hpo_id=oterm.id, label=oterm.label)
            if oterm.has_frequency():
                row = HpoaTableRow(disease=self._disease, hpo_term=hpterm, publication=self._pmid, biocurator=self._biocurator, freq_num=oterm.numerator, freq_denom=oterm.denominator)
            else:
                row = HpoaTableRow(disease=self._disease, hpo_term=hpterm, publication=self._pmid, biocurator=self._biocurator)
            rows.append(row.get_dict())
        df = pd.DataFrame.from_records(data=rows, columns=column_names)
        return df

    def write_data_frame(self):
        df = self.get_dataframe()
        dlist = df["#diseaseID"].unique()
        if len(dlist) != 1:
            raise ValueError("Error - expected to get one disease but got {len(dlist)}")
        disease = dlist[0].replace(":", "-")
        fname = f"{disease}.tab"
        df.to_csv(fname, sep="\t", index=False)
        print(f"Wrote HPOA disease file to {fname}")


class HpoaTableBuilder:

    def __init__(self, indir=None, phenopacket_list=None) -> None:
        if indir is not None:
            if not os.path.isdir(indir):
                raise ValueError(f"indir argument {indir} must be directory!")
            self._indir = indir
            self._phenopackets = []
            for file in os.listdir(indir):
                fname = os.path.join(indir, file)
                if fname.endswith(".json") and os.path.isfile(fname):
                    with open(fname) as f:
                        data = f.read()
                        jsondata = json.loads(data)
                        ppack = Parse(json.dumps(jsondata), PPKt.Phenopacket())
                        self._phenopackets.append(ppack)
        elif phenopacket_list is not None:
            self._phenopackets = phenopacket_list
        else:
            raise ValueError("A valid value must be supplied for either \"indir\" or \"phenopacket_list\"")
        self._onset_terms = []

    def embryonal_onset(self, num:int=None, denom:int=None):
        """Onset of disease at up to 8 weeks following fertilization (corresponding to 10 weeks of gestation).
        """
        oterm = OnsetTerm(onset_term_id="HP:0011460", onset_term_label="Embryonal onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def fetal_onset(self, num:int=None, denom:int=None):
        """Onset prior to birth but after 8 weeks of embryonic development (corresponding to a gestational age of 10 weeks).
        """
        oterm = OnsetTerm(onset_term_id="HP:0011461", onset_term_label="Fetal onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def second_trimester_onset(self, num:int=None, denom:int=None):
        """second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive)
        """
        oterm = OnsetTerm(onset_term_id="HP:0034198", onset_term_label="Second trimester onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def late_first_trimester_onset(self, num:int=None, denom:int=None):
        """late first trimester during the early fetal period, which is defined as 11 0/7 to 13 6/7 weeks of gestation (inclusive).
        """
        oterm = OnsetTerm(onset_term_id="HP:0034199", onset_term_label="Late first trimester onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def third_trimester_onset(self, num:int=None, denom:int=None):
        """third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
        """
        oterm = OnsetTerm(onset_term_id="HP:0034197", onset_term_label="Third trimester onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def antenatal_onset(self, num:int=None, denom:int=None):
        """onset prior to birth
        """
        oterm = OnsetTerm(onset_term_id="HP:0030674", onset_term_label="Antenatal onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def congenital_onset(self, num:int=None, denom:int=None):
        """A phenotypic abnormality that is present at birth.
        """
        oterm = OnsetTerm(onset_term_id="HP:0003577", onset_term_label="Congenital onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def neonatal_onset(self, num:int=None, denom:int=None):
        """Onset of signs or symptoms of disease within the first 28 days of life.
        """
        oterm = OnsetTerm(onset_term_id="HP:0003623", onset_term_label="Neonatal onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self


    def infantile_onset(self, num:int=None, denom:int=None):
        """Onset of signs or symptoms of disease between 28 days to one year of life.
        """
        oterm = OnsetTerm(onset_term_id="HP:0003593", onset_term_label="Infantile onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def childhood_onset(self, num:int=None, denom:int=None):
        """Onset of disease at the age of between 1 and 5 years.
        """
        oterm = OnsetTerm(onset_term_id="HP:0011463", onset_term_label="Childhood onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def juvenile_onset(self, num:int=None, denom:int=None):
        """Onset of signs or symptoms of disease between the age of 5 and 15 years.
        """
        oterm = OnsetTerm(onset_term_id="HP:0003621", onset_term_label="Juvenile onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def adult_onset(self, num:int=None, denom:int=None):
        """Onset of disease after 16 years  .
        """
        oterm = OnsetTerm(onset_term_id="HP:0003581", onset_term_label="Adult onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def young_adult_onset(self, num:int=None, denom:int=None):
        """Onset of disease at the age of between 16 and 40 years.
        """
        oterm = OnsetTerm(onset_term_id="HP:0011462", onset_term_label="Young adult onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def middle_age_onset(self, num:int=None, denom:int=None):
        """onset of symptoms at the age of 40 to 60 years.
        """
        oterm = OnsetTerm(onset_term_id="HP:0003596", onset_term_label="Middle age onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def late_onset(self, num:int=None, denom:int=None):
        """Onset of symptoms after the age of 60 years.
        """
        oterm = OnsetTerm(onset_term_id="HP:0003584", onset_term_label="Late onset", numerator=num, denominator=denom)
        self._onset_terms.append(oterm)
        return self

    def build(self):
        return HpoaTableCreator(phenopacket_list=self._phenopackets,
                                onset_term_list= self._onset_terms)



