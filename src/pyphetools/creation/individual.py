import phenopackets as PPKt
import re
import os
from typing import List, Union
from google.protobuf.json_format import MessageToJson
from .constants import Constants
from .disease import Disease
from .hp_term import HpTerm
from .hgvs_variant import Variant
from .metadata import MetaData


class Individual:
    """
    A class to represent one individual of the cohort

    :param individual_id: The individual identifier
    :type individual_id: str
    :param hpo_terms: List of HpTerm objects
    :type hpo_terms: List[pyphetools.creation.HpTerm]
    :param sex: String corresponding to the sex of the individual, default, n/a
    :type sex: str
    :param age: String corresponding to the age of the individual (ISO), default, n/a
    :type age: str
    :param interpretation_list: list of GA4GH VariationInterpretation objects
    :type interpretation_list: List[PPKt.VariationInterpretation], optional
    :param disease: object defining the disease diagnosos
    :type disease: Disease, optional
    """

    def __init__(self,
                individual_id:str,
                hpo_terms:List[HpTerm]=None,
                pmid:str=None,
                title:str=None,
                sex:str=Constants.NOT_PROVIDED,
                age:str=Constants.NOT_PROVIDED,
                interpretation_list:List[PPKt.VariantInterpretation]=None,
                disease:Disease=None):
        """Constructor
        """
        if isinstance(individual_id, int):
            self._individual_id = str(individual_id)
        elif isinstance(individual_id, str):
            self._individual_id = individual_id
        else:
            raise ValueError(f"individual_id argument must be int or string but was {type(individual_id)}")
        if sex is None:
            self._sex = PPKt.Sex.UNKNOWN_SEX
        else:
            self._sex = sex
        self._age = age
        if hpo_terms is None:
            self._hpo_terms = list()
        else:
            self._hpo_terms = hpo_terms
        if interpretation_list is None:
            self._interpretation_list = list()
        else:
            self._interpretation_list = interpretation_list
        self._disease = disease
        self._pmid = pmid
        self._title = title

    @property
    def id(self):
        """
        :returns: the individual identifier
        :rtype: str
        """
        return self._individual_id

    @property
    def sex(self):
        """
        :returns: one of 'MALE', 'FEMALE', 'OTHER', 'UNKNOWN'
        :rtype: str
        """
        return self._sex

    def set_sex(self, sex):
        self._sex = sex

    @property
    def age(self):
        """
        :returns: an iso8601 representation of age
        :rtype: str
        """
        return self._age

    def set_age(self, iso_age):
        self._age = iso_age

    @property
    def hpo_terms(self):
        """
        :returns: a list of observed and excluded HPO terms
        :rtype: List[pyphetools.creation.HpTerm]
        """
        return self._hpo_terms

    @property
    def interpretation_list(self) -> List[PPKt.VariantInterpretation]:
        """
        :returns: a list of GA4GH Genomic Interpretations
        :rtype: List[PPKt.VariantInterpretation]
        """
        return self._interpretation_list

    def add_variant(self, v:Union[Variant, PPKt.VariantInterpretation], acmg:str=None):
        """
        :param v: A Variant obeserved in this individual
        :type v: Union[Variant, PPKt.VariantInterpretation]
        :param acmg: One of the five ACMG pathogenicity categories
        :type acmg: str
        """
        if isinstance(v, Variant):
            variant = v.to_ga4gh_variant_interpretation(acmg=acmg)
        else:
            variant = v
        if isinstance(variant, PPKt.VariantInterpretation):
            self._interpretation_list.append(variant)
        else:
            raise ValueError(f"variant argument must be pyphetools Variant or GA4GH VariantInterpretation but was {type(variant)}")



    def add_hpo_term(self, term:HpTerm) -> None:
        """
        Adds one HPO term to the current individual.
        :param term: An HPO term (observed or excluded, potentially with Age of observation
        :type term: HpTerm
        """
        if not isinstance(term, HpTerm):
            raise ValueError(f"\"term\" argument must be HpTerm but was {type(term)}")
        self._hpo_terms.append(term)

    def set_disease(self, disease:Disease) -> None:
        """
        This method is typically useful for a cohort with multiple diagnoses; otherwise, the disease can be set by the
        CohortEncoder

        :param disease: the disease diagnosis for this individual
        :type disease: Disease
        """
        self._disease = disease

    def set_hpo_terms(self, cleansed_hpo_terms:List[HpTerm]):
        """
        :param cleansed_hpo_terms: a list of HpTerm objects that has been cleansed by OntologyQC
        :type cleansed_hpo_terms: List[pyphetools.creation.HpTerm]
        """
        self._hpo_terms = cleansed_hpo_terms

    @property
    def pmid(self):
        return self._pmid

    def set_pmid(self, pmid:str):
        """
        :param pmid: The PubMed identifier for the publication in which this individual was described (e.g. PMID:321..)
        :type pmid: str
        """
        self._pmid = pmid

    def get_phenopacket_id(self, phenopacket_id=None) -> str:
        """
        :returns: the Phenopacket identifier for this individual
        :rtype: str
        """
        if phenopacket_id is None:
            indi_id = self._individual_id.replace(" ", "_")
            if self._pmid is not None:
                pmid = self._pmid.replace(":", "_")
                ppkt_id = f"{pmid}_{indi_id}"
            else:
                ppkt_id = indi_id
        else:
            ppkt_id = phenopacket_id
        ppkt_id = ppkt_id.replace(" ", "_")
        return ppkt_id


    def to_ga4gh_phenopacket(self, metadata, phenopacket_id=None):
        """
        Transform the data into GA4GH Phenopacket format
        :returns:  a GA4GH Phenopacket representing this individual
        :rtype: phenopackets.Phenopacket
        """
        if isinstance(metadata, MetaData):
            metadata = metadata.to_ga4gh()
        if not isinstance(metadata, PPKt.MetaData):
            raise ValueError(f"metadata argument must be pyphetools.MetaData or GA4GH MetaData but was {type(metadata)}")
        php = PPKt.Phenopacket()
        php.id = self.get_phenopacket_id(phenopacket_id=phenopacket_id)
        php.subject.id = self._individual_id
        if self._sex == Constants.MALE_SYMBOL:
            php.subject.sex = PPKt.Sex.MALE
        elif self._sex == Constants.FEMALE_SYMBOL:
            php.subject.sex = PPKt.Sex.FEMALE
        elif self._sex == Constants.OTHER_SEX_SYMBOL:
            php.subject.sex = PPKt.Sex.OTHER_SEX
        elif self._sex == Constants.UNKOWN_SEX_SYMBOL:
            php.subject.sex = PPKt.Sex.UNKNOWN_SEX
        if self._age is not None and self._age != Constants.NOT_PROVIDED:
            php.subject.time_at_last_encounter.age.iso8601duration = self._age
        if isinstance(self._hpo_terms, list):
            for hp in self._hpo_terms:
                if not hp.measured:
                    continue
                pf = hp.to_phenotypic_feature()
                if pf.onset.age.iso8601duration is None and self._age != Constants.NOT_PROVIDED:
                    pf.onset.age.iso8601duration = self._age
                php.phenotypic_features.append(pf)
        elif isinstance(self._hpo_terms, dict):
            for age_key, hpoterm_list in self._hpo_terms.items():
                for hp in hpoterm_list:
                    if not hp.measured:
                        continue
                    pf = hp.to_phenotypic_feature()
                    # only adjust age of onset if not present
                    if pf.onset.age.iso8601duration is None and age_key.startswith("P"):
                        pf.onset.age.iso8601duration = age_key
                    php.phenotypic_features.append(pf)
        if len(self._interpretation_list) > 0:
            interpretation = PPKt.Interpretation()
            interpretation.id = self._individual_id
            interpretation.progress_status = PPKt.Interpretation.ProgressStatus.SOLVED
            if self._disease is not None:
                interpretation.diagnosis.disease.id = self._disease.id
                interpretation.diagnosis.disease.label = self._disease.label
            for var in self._interpretation_list:
                genomic_interpretation = PPKt.GenomicInterpretation()
                genomic_interpretation.subject_or_biosample_id = self._individual_id
                # by assumption, variants passed to this package are all causative
                genomic_interpretation.interpretation_status = PPKt.GenomicInterpretation.InterpretationStatus.CAUSATIVE
                genomic_interpretation.variant_interpretation.CopyFrom(var)
                interpretation.diagnosis.genomic_interpretations.append(genomic_interpretation)
            php.interpretations.append(interpretation)
        if self._pmid is not None and self._title is not None:
            # overrides the "general" setting of the external reference for the entire cohort
            metadata.external_references.clear()
            extref = PPKt.ExternalReference()
            extref.id = self._pmid
            pm = self._pmid.replace("PMID:", "")
            extref.reference = f"https://pubmed.ncbi.nlm.nih.gov/{pm}"
            extref.description = self._title
            metadata.external_references.append(extref)
        php.meta_data.CopyFrom(metadata)
        return php

    @staticmethod
    def output_individuals_as_phenopackets(individual_list, metadata:MetaData, outdir="phenopackets"):
        """write a list of Individual objects to file in GA4GH Phenopacket format

        This methods depends on the MetaData object having a PMID and will fail otherwise

        :param individual_list: List of individuals to be written to file as phenopackets
        :type individual_list: List[Individual]
        :param metadata: pyphetools MetaData object
        :type metadata: MetaData
        :param outdir: Path to output directory. Defaults to "phenopackets". Created if not exists.
        :type outdir: str
        """
        if os.path.isfile(outdir):
            raise ValueError(f"Attempt to create directory with name of existing file {outdir}")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        written = 0
        pmid = metadata.get_pmid()
        for individual in individual_list:
            phenopckt = individual.to_ga4gh_phenopacket(metadata=metadata)
            json_string = MessageToJson(phenopckt)
            if pmid is None:
                fname = "phenopacket_" + individual.id
            else:
                pmid = pmid.replace(" ", "").replace(":", "_")
                fname = pmid + "_" + individual.id
            fname = re.sub('[^A-Za-z0-9_-]', '', fname)  # remove any illegal characters from filename
            fname = fname.replace(" ", "_") + ".json"
            outpth = os.path.join(outdir, fname)
            with open(outpth, "wt") as fh:
                fh.write(json_string)
                written += 1
        print(f"We output {written} GA4GH phenopackets to the directory {outdir}")
