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




class HpoaTableCreator:
    """
    Create an HPO "small file" with the following columns
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
    These should be tab separate fields.

    """
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
        print(f"[pyphetools] Ingested {len(self._phenopackets)} GA4GH phenopackets.")
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
            d = row.get_dict()
            rows.append(d)
        df = pd.DataFrame.from_records(data=rows, columns=column_names)
        return df

