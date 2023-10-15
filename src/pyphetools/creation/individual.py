import phenopackets
import re
import os
from typing import List
from google.protobuf.json_format import MessageToJson
from .constants import Constants
from .hgvs_variant import Variant


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
    :type interpretation_list: List[VariationInterpretation], optional
    :param disease_id: String corresponding to the disease ID, default
    :type disease_id: str, optional
    :param disease_label: String corresponding to the disease label, default
    :type disease_label: str, optional
    """

    def __init__(self, individual_id,
                 hpo_terms,
                 pmid=None,
                 sex=Constants.NOT_PROVIDED,
                 age=Constants.NOT_PROVIDED,
                 interpretation_list=None,
                 disease_id=None,
                 disease_label=None):
        """Constructor
        """
        if isinstance(individual_id, int):
            self._individual_id = str(individual_id)
        elif isinstance(individual_id, str):
            self._individual_id = individual_id
        else:
            raise ValueError(f"individual_id argument must be int or string but was {type(individual_id)}")
        if sex is None:
            self._sex = phenopackets.Sex.UNKNOWN_SEX
        else:
            self._sex = sex
        self._age = age
        self._hpo_terms = hpo_terms
        self._interpretation_list = interpretation_list
        self._disease_id = disease_id
        self._disease_label = disease_label
        self._pmid = pmid

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

    @property
    def age(self):
        """
        :returns: an iso8601 representation of age
        :rtype: str
        """
        return self._age

    @property
    def hpo_terms(self):
        """
        :returns: a list of observed and excluded HPO terms
        :rtype: List[pyphetools.creation.HpTerm]
        """
        return self._hpo_terms

    @property
    def interpretation_list(self):
        """
        :returns: a list of GA4GH Genomic Interpretations
        :rtype:
        """
        return self._interpretation_list

    def add_variant(self, v, acmg=None):
        """
        :param v: A Variant obeserved in this individual
        :type v: Variant
        :param acmg: One of the five ACMG pathogenicity categories
        :type acmg: str
        """
        if not isinstance(v, Variant):
            raise ValueError(f"variant argument must be pyphetools Variant type but was {type(v)}")
        self._interpretation_list.append(v.to_ga4gh_variant_interpretation(acmg=acmg))


    def set_disease(self, disease_id, disease_label):
        """
        Set the disease diagnosis for this individual

        This method is typically useful for a cohort with multiple diagnoses; otherwise, the disease can be set by the
        CohortEncoder

        :param disease_id: The disease identifier, typically a CURIE such as OMIM:600432
        :type disease_id: str
        :param disease_label: The disease name
        :type disease_label: str
        """
        self._disease_id = disease_id
        self._disease_label = disease_label

    def set_hpo_terms(self, cleansed_hpo_terms):
        """
        :param cleansed_hpo_terms: a list of HpTerm objects that has been cleansed by OntologyQC
        :type cleansed_hpo_terms: List[pyphetools.creation.HpTerm]
        """
        self._hpo_terms = cleansed_hpo_terms

    def to_ga4gh_phenopacket(self, metadata, phenopacket_id=None):
        """_summary_
        Transform the data into GA4GH Phenopacket format
        :returns:  a GA4GH Phenopacket representing this individual
        :
        """
        if not str(type(metadata)) == "<class 'phenopackets.schema.v2.core.meta_data_pb2.MetaData'>":
            raise ValueError(f"metadata argument must be GA4GH Phenopacket Schema MetaData but was {type(metadata)}")
        php = phenopackets.Phenopacket()
        indi_id = self._individual_id.replace(" ", "_")
        if phenopacket_id is None:
            if self._pmid is not None:
                pmid = self._pmid.replace(":", "_")
                ppkt_id = f"{pmid}_{indi_id}"
            else:
                ppkt_id = indi_id
        else:
            ppkt_id = phenopacket_id
        php.id = ppkt_id.replace(" ", "_")
        php.subject.id = self._individual_id
        if self._sex == Constants.MALE_SYMBOL:
            php.subject.sex = phenopackets.Sex.MALE
        elif self._sex == Constants.FEMALE_SYMBOL:
            php.subject.sex = phenopackets.Sex.FEMALE
        elif self._sex == Constants.OTHER_SEX_SYMBOL:
            php.subject.sex = phenopackets.Sex.OTHER_SEX
        elif self._sex == Constants.UNKOWN_SEX_SYMBOL:
            php.subject.sex = phenopackets.Sex.UNKNOWN_SEX
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
            interpretation = phenopackets.Interpretation()
            interpretation.id = self._individual_id
            interpretation.progress_status = phenopackets.Interpretation.ProgressStatus.SOLVED
            if self._disease_id is not None and self._disease_label is not None:
                interpretation.diagnosis.disease.id = self._disease_id
                interpretation.diagnosis.disease.label = self._disease_label
            for var in self._interpretation_list:
                genomic_interpretation = phenopackets.GenomicInterpretation()
                genomic_interpretation.subject_or_biosample_id = self._individual_id
                # by assumption, variants passed to this package are all causative
                genomic_interpretation.interpretation_status = phenopackets.GenomicInterpretation.InterpretationStatus.CAUSATIVE
                genomic_interpretation.variant_interpretation.CopyFrom(var)
                interpretation.diagnosis.genomic_interpretations.append(genomic_interpretation)
            php.interpretations.append(interpretation)
        if metadata is not None:
            php.meta_data.CopyFrom(metadata)
        return php

    @staticmethod
    def output_individuals_as_phenopackets(individual_list, metadata, pmid=None, outdir="phenopackets"):
        """write a list of Individial objects to file in GA4GH Phenopacket format

        Args:
            individual_list (list): list of Individual's
            metadata (MetaData): GA4GH Phenopacket Schema MetaData object
            pmid (str, optional): A string such as PMID:3415687. Defaults to None.
            outdir (str, optional): Path to output directory. Defaults to "phenopackets". Created if not exists.

        Returns:
            int: number of phenopackets written
        """
        if os.path.isfile(outdir):
            raise ValueError(f"Attempt to create directory with name of existing file {outdir}")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        written = 0
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
