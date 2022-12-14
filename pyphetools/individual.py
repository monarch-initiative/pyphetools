import phenopackets 
from .variant import Variant



class Individual:
    """
    A class to represent one individual of the cohort
    """
    def __init__(self, individual_id, sex, age, hpo_terms, variant_list) -> None:
        """
        Represents all of the data we will transform into a single phenopacket
        """
        self._individual_id = str(individual_id) 
        self._sex = sex
        self._age = age
        self._hpo_terms = hpo_terms
        self._variant_list = variant_list
        
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
    
    def to_ga4gh_phenopacket(self):
        """_summary_
        Transform the data into GA4GH Phenopacket format
        Returns:
            _type_: _description_
        """
        php = phenopackets.Phenopacket()
        php.id = self._individual_id
        php.subject.id = self._individual_id
        if self._sex == 'M':
            php.subject.sex = phenopackets.Sex.MALE
        elif self._sex == 'F':
            php.subject.sex = phenopackets.Sex.FEMALE
        php.subject.time_at_last_encounter.age.iso8601duration = "P2Y"  ## TODO -- we need to code age with ISO
        for hp in self._hpo_terms:
            if not hp.measured:
                continue
            pf = phenopackets.PhenotypicFeature()
            pf.type.id = hp.id
            pf.type.label = hp.label
            if not hp.observed:
                pf.excluded = True
            php.phenotypic_features.append(pf)
        #if len(self._variant_list) > 0:
        #    for var in self._variant_list:
                
        return php