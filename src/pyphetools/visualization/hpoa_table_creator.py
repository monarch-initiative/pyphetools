import os
import json
from typing import List, Dict

from google.protobuf.json_format import Parse

from ..creation.disease import Disease
from ..creation.hp_term import HpTerm
from ..creation.individual import Individual
from ..creation.metadata import MetaData
from .counted_hpo_term import CountedHpoTerm, CohortTermCounter
from .onset_calculator import OnsetCalculator

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



class HpoaPmidCounter:
    def __init__(self) -> None:
        self._observed = defaultdict(int)
        self._measured = defaultdict(int)

    def increment_observed(self, hpo_id:str):
        self._observed[hpo_id] += 1

    def increment_measured(self, hpo_id:str):
        self._measured[hpo_id] += 1

    def get_observed_d(self):
        return self._observed

    def get_measured_d(self):
        return self._measured


class HpoaOnsetCounter:
    def __init__(self) -> None:
        self._onset = defaultdict(int)

    def increment_onset(self, hpo_id:str):
        self._onset[hpo_id] += 1

    def get_onset_numerator_d(self):
        return self._onset

    def get_onset_denominator(self):
        d = sum([v for v in self._onset.values()])
        if d == 0:
            raise ValueError(f"Attempt to use HpoaOnsetCounter with no data")
        return d



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
    def __init__(self, phenopacket_list, onset_term_d,  moi_d, created_by:str=None) -> None:
        """Constructor

        :param phenopacket_list: List of GA4GH phenopackets
        :type phenopacket_list: List[PPKt.Phenopacket]
        :param onset_term_d: Dictionary with key PMID string and value: OnsetTerm object
        :type: Dict[str, OnsetTerm]
        :param moi_d: Dictionary with key PMID and value Mode of inheritance
        """
        self._phenopackets = phenopacket_list
        self._created_by = created_by
        self._all_hpo_d = self._get_all_hpos()
        self._disease = self._get_disease() # only allow one disease, therefore this is a scalar value (string)
        self._hpo_counter_d = self._count_hpos()
        self._biocurator_d = self._get_biocurator_d()
        self._onset_rows = self._add_age_of_onset_terms(onset_term_d)
        self._moi_rows = self._add_moi_rows(moi_d)
        

    def _get_all_hpos(self) -> Dict[str,HpTerm]:
        """Get a dictionary of HpTerms, with key being HPO id and the value the corresponding HpTerm

        We use this to retrieve the label
        :returns: a dictionary, with key=HPO id, value: HpTerm
        :rtype: Dict[str, HpTerm]
        """
        all_hpo_d = {}
        for ppkt in self._phenopackets:
            for pf in ppkt.phenotypic_features:
                hpterm = HpTerm(hpo_id=pf.type.id, label=pf.type.label)
                all_hpo_d[hpterm.id] = hpterm
        print(f"We found a total of {len(all_hpo_d)} unique HPO terms")
        return all_hpo_d


    @staticmethod
    def get_pmid(ppkt):
        mdata = ppkt.meta_data
        if mdata.external_references is None:
            raise ValueError("MetaData must have external_references element for HPOA conversion")
        eref_list = mdata.external_references
        if len(eref_list) != 1:
            raise ValueError(f"MetaData must have exactly one external_references element for HPOA conversion but had {len(eref_list)}")
        eref = eref_list[0]
        pmid = eref.id
        if not pmid.startswith("PMID:"):
            raise ValueError(f"Malformed PMID: \"{pmid}\"")
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
            disease_lst = '; '.join([disease.id for disease in disease_set])
            raise ValueError(f"Error: must have only a single Disease for HPOA conversion but we found {len(disease_set)}: {disease_lst}")
        [disease] = disease_set
        print(f"Extracted disease: {disease}")
        return disease

    def _get_biocurator_d(self):
        """The unspoken assumption of this function is that there is just one biocurator per PMID.
        This will be true for phenopackets created by pyphetools.

        :returns: dictionary with key=PMID, value=biocurator
        :rtype: Dict[str,str]
        """
        biocurator_d = defaultdict()
        for ppkt in self._phenopackets:
            pmid = HpoaTableCreator.get_pmid(ppkt=ppkt)
            mdata = ppkt.meta_data
            created_by = mdata.created_by
            biocurator_d[pmid] = created_by
        return biocurator_d

    def _count_hpos(self):
        hpo_counter_d = defaultdict(HpoaPmidCounter)
        for ppkt in self._phenopackets:
            pmid = HpoaTableCreator.get_pmid(ppkt=ppkt)
            hpo_counter = hpo_counter_d.get(pmid)
            # if not yet present,  initialize with zero counts
            if  hpo_counter is None:
                hpo_counter = HpoaPmidCounter()
                hpo_counter_d[pmid] = hpo_counter
            for pf in ppkt.phenotypic_features:
                hpterm = HpTerm(hpo_id=pf.type.id, label=pf.type.label)
                hpo_counter.increment_measured(hpterm.id)
                if pf.excluded is not None and not pf.excluded:
                    hpo_counter.increment_observed(hpterm.id)
        return hpo_counter_d

    def _add_age_of_onset_terms(self, onset_term_d) -> List[HpoaTableRow]:
        """
        :param onset_term_d: Dictionary with key=pmid, value: list of CountedHpoTerm objects
        :type onset_term_d: Dict[str, List[CountedHpoTerm]]
        """
        onset_rows  = list() # reset
        for pmid, oterm_list in onset_term_d.items():
            biocurator = self._biocurator_d.get(pmid)
            for oterm in oterm_list:
                hpo_onset_term = HpTerm(hpo_id=oterm.id, label=oterm.label)
                row = HpoaTableRow(disease=self._disease, hpo_term=hpo_onset_term, publication=pmid, biocurator=biocurator, freq_num=oterm.numerator, freq_denom=oterm.denominator)
                onset_rows.append(row)
        return onset_rows

    def _add_moi_rows(self, moi_d) -> List[HpoaTableRow]:
        """Add mode of inheritance information
        :param moi_d: dictionary with key: PMID, and value: List of MOI terms
        :type moi_d:Dict[str,List[str]]
        :returns: list of HPOA table rows
        :rtype: List[HpoaTableRow]
        """
        moi_rows = list()
        for pmid, hpterm_list in moi_d.items():
            biocurator = self._biocurator_d.get(pmid)
            # If we add an MOI outside of the template, then it will not have a PMID
            # the template builder requires a created_by field which is designed for this.
            if biocurator is None:
                biocurator = self._created_by
            for hpterm in hpterm_list:
                row = HpoaTableRow(disease=self._disease, hpo_term=hpterm, publication=pmid, biocurator=biocurator)
                moi_rows.append(row)
        return moi_rows


    def get_dataframe(self):
        rows = []
        column_names = ["#diseaseID", "diseaseName", "phenotypeID", "phenotypeName",
                        "onsetID", "onsetName", "frequency", "sex", "negation",  "modifier",
                        "description", "publication","evidence", "biocuration"]
        for pmid, counter in self._hpo_counter_d.items():
            biocurator = self._biocurator_d.get(pmid)
            measured_d = counter.get_measured_d()
            observed_d = counter.get_observed_d()
            # by construction, there can be no term in observed_d that is not in measured_d
            for hpo_id in measured_d:
                n = observed_d.get(hpo_id, 0)
                m = measured_d.get(hpo_id)
                hpo_term = self._all_hpo_d.get(hpo_id)
                row = HpoaTableRow(disease=self._disease, hpo_term=hpo_term, publication=pmid, biocurator=biocurator, freq_num=n, freq_denom=m)
                rows.append(row.get_dict())
        for onset_row in self._onset_rows:
            rows.append(onset_row.get_dict())
        for moi_row in self._moi_rows:
            rows.append(moi_row.get_dict())
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

    def __init__(self, indir=None, phenopacket_list=None, created_by:str=None) -> None:
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
        self._onset_term_d = defaultdict(list)
        self._moi_d = defaultdict(list)
        self._created_by = created_by
        onset_calc = OnsetCalculator(self._phenopackets)
        pmid_onset_d = onset_calc.get_pmid_to_onset_d()
        for pmid, onset_list in pmid_onset_d.items():
            tcounter = CohortTermCounter(pmid=pmid)
            for onset in onset_list:
                tcounter.increment_term(onset)
            self._onset_term_d[pmid].extend(tcounter.get_counted_terms())

    def autosomal_recessive(self, pmid):
        moi_term = HpTerm(hpo_id="HP:0000007", label="Autosomal recessive inheritance")
        self._moi_d[pmid].append(moi_term)
        return self

    def autosomal_dominant(self, pmid):
        moi_term = HpTerm(hpo_id="HP:0000006", label="Autosomal dominant inheritance")
        self._moi_d[pmid].append(moi_term)
        return self

    def x_linked(self, pmid):
        moi_term = HpTerm(hpo_id="HP:0001417", label="X-linked inheritance")
        self._moi_d[pmid].append(moi_term)
        return self

    def x_linked_recessive(self, pmid):
        moi_term = HpTerm(hpo_id="HP:0001419", label="X-linked recessive inheritance")
        self._moi_d[pmid].append(moi_term)
        return self

    def x_linked_dominant(self, pmid):
        moi_term = HpTerm(hpo_id="HP:0001423", label="X-linked dominant inheritance")
        self._moi_d[pmid].append(moi_term)
        return self


    def build(self):
        return HpoaTableCreator(phenopacket_list=self._phenopackets, onset_term_d=self._onset_term_d, moi_d=self._moi_d, created_by=self._created_by)

    @staticmethod
    def from_individuals(individual_list:List[Individual], created_by:str):
        """Create builder object from list of individuals
        This can be easier than needed to create phenopacket objects in a workbook
        The method requires that each Individual object have a Citation

        :param individual_list: List of individuals to be summarized in HPOA format
        :type individual_list: List[Individual]
        :param created_by: the ORCID id of the person who biocurated the data
        :type created_by: str
        :returns: HPOA table builder object
        :rtype: HpoaTableBuilder
        """
        ppkt_list = list()
        for i in individual_list:
            cite = i.get_citation()
            metadata = MetaData(created_by=created_by, citation=cite)
            ppkt = i.to_ga4gh_phenopacket(metadata=metadata)
            ppkt_list.append(ppkt)
        return HpoaTableBuilder(phenopacket_list=ppkt_list)




