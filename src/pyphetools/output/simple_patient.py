import os
import phenopackets
#from phenopackets import Phenopacket
from google.protobuf.json_format import Parse
import json
from collections import defaultdict

from ..creation.hp_term import HpTerm
from .simple_variant import SimpleVariant

class SimplePatient:
    """
    This class flattens all observed terms into a set and also recorded variants, sex, identifier, and age
    The class purposefully disregards information about the time course in order to be able to count the 
    frequencies of HPO terms in groups
    """

    def __init__(self, ga4gh_phenopacket) -> None:
        # in this case, ga4gh_phenopacket cannot be None
        if str(type(ga4gh_phenopacket)) != "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":                   
            raise ValueError(f"phenopacket argument must be GA4GH Phenopacket Schema Phenopacket but was {type(ga4gh_phenopacket)}")
        else:
            ppack = ga4gh_phenopacket
        observed_hpo_terms = defaultdict(HpTerm)
        excluded_hpo_terms = defaultdict(HpTerm)
        self._phenopacket_id = ppack.id
        if ppack.subject is None:
            raise ValueError("Phenopackets must have a subject message to be used with this package")
        subj = ppack.subject
        if subj.id is None:
            raise ValueError("Phenopacket subjects must have an id field to be used with this package")
        else:
            self._subject_id = subj.id
        if subj.time_at_last_encounter is None or subj.time_at_last_encounter.age.iso8601duration is None:
            print("Warning: No age found for phenopacket")
            self._time_at_last_encounter = None
        else:
            self._time_at_last_encounter = subj.time_at_last_encounter.age.iso8601duration 
        if ppack.subject.sex == phenopackets.MALE:
            self._sex = "MALE"
        elif ppack.subject.sex == phenopackets.FEMALE:
            self._sex = "FEMALE"
        elif ppack.subject.sex == phenopackets.OTHER_SEX:
            self._sex = "OTHER"
        else:
            self._sex = "UNKNOWN"
        for pf in ppack.phenotypic_features:
            hpterm = HpTerm(hpo_id=pf.type.id, label=pf.type.label, observed=not pf.excluded)
            if pf.excluded:
                excluded_hpo_terms[pf.type.id] = hpterm
            else:
                observed_hpo_terms[pf.type.id] = hpterm
        for k, v in observed_hpo_terms.items():
            if k in excluded_hpo_terms:
                excluded_hpo_terms.pop(k) # remove observed terms that may have been excluded at other occasion
        self._observed = observed_hpo_terms
        self._excluded = excluded_hpo_terms
        # Add information about variants
        self._variant_list = []
        if ppack.interpretations is not None and len(ppack.interpretations) > 0:
            interprets = ppack.interpretations
            for interpretation in interprets:
                if str(type(interpretation)) != "<class 'phenopackets.schema.v2.core.interpretation_pb2.Interpretation'>":
                    raise ValueError(f"interpretation argument must be GA4GH Phenopacket Interpretation but was {type(interpretation)}")
                diagnosis = interpretation.diagnosis
                ginterpretations = diagnosis.genomic_interpretations
                for gint in ginterpretations:
                    variant = SimpleVariant(ginterpretation=gint)
                    self._variant_list.append(variant)
        # TODO -- add information about disease, ensuring that all Variants are associated with the same diagnosis
                
        
    @staticmethod
    def from_file(phenopacket_file):
        """
        Return a SimplePatient object that corresponds to a phenopacket (JSON) file
        :param phenopacket_file: A phenopacket file (JSON format) 
        :type ppkt_file: string representing a path to a file
        """
        if not os.path.isfile(phenopacket_file):
            raise FileNotFoundError(f"Could not find phenopacket file at '{phenopacket_file}'") 
        with open(phenopacket_file) as f:
            data = f.read()
            jsondata = json.loads(data)
            ppack = Parse(json.dumps(jsondata), phenopackets.Phenopacket())
            return SimplePatient(ga4gh_phenopacket=ppack)
        

    @staticmethod
    def from_individual(individual, metadata):
        """
        Return a SimplePatient object that corresponds to a pyphetools Individual object
        :param individual: Am Individual object
        :type individual: Individual
        :param metadata: A GA4GH Phenopacket Schema MetaData object
        :type metadata: MetaData
        """
        ppack = individual.to_ga4gh_phenopacket(metadata)
        return SimplePatient(ga4gh_phenopacket=ppack)


    def get_phenopacket_id(self):
        return self._phenopacket_id

    def get_subject_id(self):
        return self._subject_id

    def get_sex(self):
        return self._sex

    def get_age(self):
        return self._time_at_last_encounter

    def get_observed_hpo_d(self):
        """
        returns map with key (string) HP id, value, HpTerm from creation submodule
        """
        return self._observed

    def get_excluded_hpo_d(self):
        return self._excluded

    def get_variant_list(self):
        return self._variant_list
