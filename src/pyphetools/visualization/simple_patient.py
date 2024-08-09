import os
import phenopackets
from google.protobuf.json_format import Parse
import typing
import json
import typing
from collections import defaultdict
from ..creation.constants import Constants
from ..creation.hp_term import HpTerm
from ..creation.individual import Individual
from ..creation.pyphetools_age import IsoAge, NoneAge
from .simple_variant import SimpleVariant
from ..pp.v202 import VitalStatus

class SimplePatient:
    """
    This class flattens all observed terms into a set and also recorded variants, sex, identifier, and age
    The class purposefully disregards information about the time course in order to be able to count the
    frequencies of HPO terms in groups. The use case of the class is to facilitate visualization of
    a collection of phenopackets from files or that have just been ingested using pyphetools. Each simple
    patient is essentially a wrapper around one phenopacket.

    :param ga4gh_phenopacket: A Phenopacket object representing one individual
    :type ga4gh_phenopacket: phenopackets.schema.v2.phenopackets_pb2.Phenopacket
    """

    def __init__(self, ga4gh_phenopacket) -> None:
        if str(type(ga4gh_phenopacket)) != "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":
            raise ValueError(f"phenopacket argument must be GA4GH Phenopacket Schema Phenopacket but was {type(ga4gh_phenopacket)}")
        else:
            ppack = ga4gh_phenopacket
        self._observed_hpo_terms = defaultdict(HpTerm)
        self._excluded_hpo_terms = defaultdict(HpTerm)
        self._by_age_dictionary = defaultdict(list)
        self._phenopacket_id = ppack.id
        if not ppack.HasField("subject"):
            raise ValueError("Phenopackets must have a subject message to be used with this package")
        subj = ppack.subject
        if not subj.id:
            # This means the subject identifier was not set. This should never happen but is not critical.
            self._subject_id = self._phenopacket_id
        else:
            self._subject_id = subj.id
        self._time_at_last_encounter = None
        if subj.HasField("time_at_last_encounter"):
            time_at_last_encounter = phenopackets.TimeElement()
            time_at_last_encounter.CopyFrom(subj.time_at_last_encounter)
            if time_at_last_encounter.HasField("age"):
                self._time_at_last_encounter = time_at_last_encounter.age.iso8601duration
            elif time_at_last_encounter.HasField("ontology_class"):
                clz = time_at_last_encounter.ontology_class
                self._time_at_last_encounter = f"{clz.label} ({clz.id})"
        if ppack.subject.sex == phenopackets.MALE:
            self._sex = "MALE"
        elif ppack.subject.sex == phenopackets.FEMALE:
            self._sex = "FEMALE"
        elif ppack.subject.sex == phenopackets.OTHER_SEX:
            self._sex = "OTHER"
        else:
            self._sex = "UNKNOWN"
        ## get vital status if possible
        self._vstat = None
        self._survival_time_in_days = None
        self._cause_of_death = None
        if ppack.subject.HasField("vital_status"):
            vstat = ppack.subject.vital_status
            if vstat.status == VitalStatus.Status.DECEASED:
                self._vstat = "DECEASED"
            elif vstat.status == VitalStatus.Status.ALIVE:
                self._vstat = "ALIVE"
            else:
                pass # keep self._vstat as None
            if vstat.survival_time_in_days is not None:
                self._survival_time_in_days = vstat.survival_time_in_days
            self._cause_of_death = vstat.cause_of_death
       
        for pf in ppack.phenotypic_features:
            hpterm = HpTerm(hpo_id=pf.type.id, label=pf.type.label, observed=not pf.excluded)
            if pf.excluded:
                self._excluded_hpo_terms[pf.type.id] = hpterm
            else:
                self._observed_hpo_terms[pf.type.id] = hpterm
            if pf.onset is not None and pf.onset.age is not None and pf.onset.age.iso8601duration:
                term_onset = pf.onset.age.iso8601duration
            else:
                term_onset = Constants.NOT_PROVIDED
            self._by_age_dictionary[term_onset].append(hpterm)
        for k, v in self._observed_hpo_terms.items():
            if k in self._excluded_hpo_terms:
                self._excluded_hpo_terms.pop(k) # remove observed terms that may have been excluded at other occasion
        # Add information about variants
        self._variant_list = []
        self._disease = None
        if ppack.interpretations is not None and len(ppack.interpretations) > 0:
            interprets = ppack.interpretations
            for interpretation in interprets:
                if str(type(interpretation)) != "<class 'phenopackets.schema.v2.core.interpretation_pb2.Interpretation'>":
                    raise ValueError(f"interpretation argument must be GA4GH Phenopacket Interpretation but was {type(interpretation)}")
                diagnosis = interpretation.diagnosis
                if diagnosis is not None:
                    if diagnosis.disease is not None:
                        disease_id = diagnosis.disease.id
                        disease_label = diagnosis.disease.label
                        self._disease = f"{disease_label} ({disease_id})"
                ginterpretations = diagnosis.genomic_interpretations
                for gint in ginterpretations:
                    variant = SimpleVariant(ginterpretation=gint)
                    self._variant_list.append(variant)
        # Get PMID, if available, from the MetaData
        mdata = ppack.meta_data
        self._pmid = None
        if len(mdata.external_references) == 1:
            eref = mdata.external_references[0]
            self._pmid = eref.id

    @staticmethod
    def from_file(phenopacket_file: str) -> "SimplePatient":
        """
        Return a SimplePatient object that corresponds to a phenopacket (JSON) file
        :param phenopacket_file: A phenopacket file (JSON format)
        :type phenopacket_file: string representing a path to a file
        """
        if not os.path.isfile(phenopacket_file):
            raise FileNotFoundError(f"Could not find phenopacket file at '{phenopacket_file}'")
        with open(phenopacket_file) as f:
            data = f.read()
            jsondata = json.loads(data)
            ppack = Parse(json.dumps(jsondata), phenopackets.Phenopacket())
            return SimplePatient(ga4gh_phenopacket=ppack)


    @staticmethod
    def from_individual(individual: Individual, metadata):
        """
        Return a SimplePatient object that corresponds to a pyphetools Individual object
        :param individual: Am Individual object
        :type individual: Individual
        :param metadata: A GA4GH Phenopacket Schema MetaData object
        :type metadata: MetaData
        """
        ppack = individual.to_ga4gh_phenopacket(metadata)
        return SimplePatient(ga4gh_phenopacket=ppack)


    def get_phenopacket_id(self) -> str:
        return self._phenopacket_id

    def get_subject_id(self) -> str:
        return self._subject_id

    def get_sex(self):
        return self._sex

    def get_age(self)-> typing.Optional[str]:
        return self._time_at_last_encounter
    
    @staticmethod
    def age_in_years(iso_age:str) -> typing.Optional[float]:
        if iso_age is None:
            return None
        if isinstance(iso_age, NoneAge):
            return None
        if len(iso_age) == 0:
            return None
        if not iso_age.startswith("P"):
            print(f"ERROR-isoage malformed: {iso_age}")
            return None
        ppt_age = IsoAge.from_iso8601(iso_age=iso_age)
        years = ppt_age.years + (1/12) * ppt_age.months + (1/365) * ppt_age.days
        return years
        
    
    def get_age_in_years(self) -> typing.Optional[float]:
        if self._time_at_last_encounter is None or not self._time_at_last_encounter:
            return None
        return SimplePatient.age_in_years(iso_age=self._time_at_last_encounter)
       

    def get_disease(self) -> str:
        return self._disease or "n/a"

    def get_observed_hpo_d(self):
        """
        returns map of observed phenotypic features with key (string) HP id, value, HpTerm from creation submodule
        """
        return self._observed_hpo_terms

    def get_excluded_hpo_d(self):
        """
        :return: map of excluded phenotypic features with key (string) HP id, value, HpTerm from creation submodule
        """
        return self._excluded_hpo_terms

    def get_total_hpo_count(self):
        """
        :return: total count of HPO terms (observed and excluded)
        :rtype: int
        """
        return len(self._observed_hpo_terms) + len(self._excluded_hpo_terms)

    def get_variant_list(self):
        return self._variant_list

    def has_pmid(self):
        return self._pmid is not None

    def get_pmid(self):
        return self._pmid

    def contains_observed_term_id(self, hpo_term_id) -> bool:
        return hpo_term_id in self._observed_hpo_terms

    def contains_excluded_term_id(self, hpo_term_id) -> bool:
        return hpo_term_id in self._excluded_hpo_terms
    
    def get_observed_term_by_id(self, hpo_term_id) -> typing.Optional[HpTerm]:
        return self._observed_hpo_terms.get(hpo_term_id)
    
    def get_excluded_term_by_id(self, hpo_term_id)-> typing.Optional[HpTerm]:
        return self._excluded_hpo_terms.get(hpo_term_id)
    
    
    def get_term_by_age_dict(self):
        return self._by_age_dictionary
    


