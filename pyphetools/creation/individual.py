import phenopackets 
from .variant import Variant
from .constants import *


class Individual:
    """
    A class to represent one individual of the cohort
    """
    def __init__(self, individual_id, sex, age, hpo_terms, variant_list=None, disease_id=None, disease_label=None):
        """
        Represents all of the data we will transform into a single phenopacket
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
        self._variant_list = variant_list
        self._disease_id = disease_id
        self._disease_label = disease_label
        
    @property
    def id(self):
        return self._individual_id
    
    @property
    def sex(self):
        return self._sex
    
    @property
    def age(self):
        return self._age
    
    @property
    def hpo_terms(self):
        return self._hpo_terms
    
    @property
    def variant_list(self):
        return self._variant_list
    
    def to_ga4gh_phenopacket(self, metadata, phenopacket_id=None):
        """_summary_
        Transform the data into GA4GH Phenopacket format
        Returns:
            _type_: _description_
        """
        if not str(type(metadata)) == "<class 'phenopackets.schema.v2.core.meta_data_pb2.MetaData'>":
            raise ValueError(f"metadata argument must be GA4GH Phenopacket Schema MetaData but was {type(metadata)}")
        php = phenopackets.Phenopacket()
        if phenopacket_id is None:
            php.id = self._individual_id
        else:
            php.id = phenopacket_id
        php.subject.id = self._individual_id
        if self._sex == MALE_SYMBOL:
            php.subject.sex = phenopackets.Sex.MALE
        elif self._sex == FEMALE_SYMBOL:
            php.subject.sex = phenopackets.Sex.FEMALE
        elif self._sex == OTHER_SEX_SYMBOL:
            php.subject.sex = phenopackets.Sex.OTHER
        elif self._sex == UNKOWN_SEX_SYMBOL:
            php.subject.sex = phenopackets.Sex.UNKNOWN
        if self._age is not None:
            php.subject.time_at_last_encounter.age.iso8601duration = self._age
        if isinstance(self._hpo_terms, list):
            for hp in self._hpo_terms:
                if not hp.measured:
                    continue
                pf = phenopackets.PhenotypicFeature()
                pf.type.id = hp.id
                pf.type.label = hp.label
                if not hp.observed:
                    pf.excluded = True
                if self._age is not None:
                    pf.onset.age.iso8601duration = self._age
                php.phenotypic_features.append(pf)
        elif isinstance(self._hpo_terms, dict):
            for age_key, hpoterm_list in self._hpo_terms.items():
                for hp in hpoterm_list:
                    if not hp.measured:
                        continue
                    pf = phenopackets.PhenotypicFeature()
                    pf.type.id = hp.id
                    pf.type.label = hp.label
                    if not hp.observed:
                        pf.excluded = True
                    if age_key.startswith("P"):
                        # Note sometimes we have no age, then use N/A -- TODO think of robust way to do this
                        pf.onset.age.iso8601duration = age_key
                    php.phenotypic_features.append(pf)
        if len(self._variant_list) > 0:
            interpretation = phenopackets.Interpretation()
            interpretation.id = self._individual_id
            interpretation.progress_status = phenopackets.Interpretation.ProgressStatus.SOLVED
            if self._disease_id is not None and self._disease_label is not None:
                interpretation.diagnosis.disease.id = self._disease_id
                interpretation.diagnosis.disease.label = self._disease_label
            for var in self._variant_list:
                genomic_interpretation = phenopackets.GenomicInterpretation()
                genomic_interpretation.subject_or_biosample_id = self._individual_id
                # by assumption, variants passed to this package are all causative
                genomic_interpretation.interpretation_status = phenopackets.GenomicInterpretation.InterpretationStatus.CAUSATIVE
                genomic_interpretation.variant_interpretation.CopyFrom(var.to_ga4gh())
                interpretation.diagnosis.genomic_interpretations.append(genomic_interpretation)
            php.interpretations.append(interpretation)
        if metadata is not None:
            php.meta_data.CopyFrom(metadata)
        return php