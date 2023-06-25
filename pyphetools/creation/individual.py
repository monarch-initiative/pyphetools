import phenopackets 
import re
import os
from google.protobuf.json_format import MessageToJson
from .constants import Constants
from .variant import Variant


class Individual:
    """
    A class to represent one individual of the cohort
    """
    def __init__(self,  individual_id, 
                        hpo_terms, 
                        sex=Constants.NOT_PROVIDED, 
                        age=Constants.NOT_PROVIDED, 
                        variant_list=None, 
                        disease_id=None, 
                        disease_label=None):
        """All of the data we will transform into a single phenopacket
        
        Args:
            individual_id (str): The individual identifier
            hpo_terms (list): List of HpTerm objects
            sex (str): String corresponding to the sex of the individual, default, n/a
            age (str): String corresponding to the age of the individual (ISO), default, n/a
            variant_list (list): list of Variant objects (optional)
            disease_id (str): String corresponding to the disease ID, default, (optional)
            disease_label (str): String corresponding to the disease label, default, (optional)
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
    
    def add_variant(self, v):
        if not isinstance(v, Variant):
            raise ValueError(f"variant argument must be pyphetools Variant type but was {type(v)}")
        self._variant_list.append(v)
    
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
        if not os.path.isdir(outdir):
            os.makedir(outdir)
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
            fname = fname.replace(" ", "_")
            outpth = os.path.join(outdir, fname, ".json")
            with open(outpth, "wt") as fh:
                fh.write(json_string)
                written += 1
        return written