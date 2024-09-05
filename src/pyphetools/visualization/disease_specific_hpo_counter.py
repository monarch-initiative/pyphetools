import typing
from collections import defaultdict
import pandas as pd
import hpotk
import phenopackets as PPKt
from ..creation.hpo_parser import HpoParser
from ..pp.v202 import Phenopacket as Phenopacket202
from ..pp.v202 import OntologyClass as OntologyClass202

TARGET_DISEASE_ID = "MONDO:0000001"

class HpoCohortCount:
    """
    Keep track of the observed and excluded counts for some HPO term within a cohort defined by a Disease
    """

    def __init__(self, hpo: OntologyClass202) -> None:
        self._hpo = hpo
        self._d_to_observed = defaultdict(int)
        self._d_to_excluded = defaultdict(int)
        self._disease_set = set()


    @property
    def hpo_display(self) -> str:
        return f"{self._hpo.label} ({self._hpo.id})"
    
    @property
    def hpo(self) -> OntologyClass202:
        return self._hpo
    

    def get_observed(self, disease: OntologyClass202) -> int:
        return self._d_to_observed[disease]
    
  
    def get_excluded(self, disease: OntologyClass202) -> int:
        return self._d_to_excluded[disease]
    
    def get_total(self) -> int:
        x = [x for x in self._d_to_observed.values()]
        return sum(x)
    
    def increment_excluded(self, disease: OntologyClass202) -> None:
        self._disease_set.add(disease)
        self._d_to_excluded[disease] += 1

    def increment_observed(self, disease: OntologyClass202) -> None:
        self._disease_set.add(disease)
        self._d_to_observed[disease] += 1

    def frequency_for_disease(self, disease: OntologyClass202) -> str:
        exc = self._d_to_excluded[disease]
        obs = self._d_to_observed[disease]
        total = exc + obs
        if total == 0:
            return "n/a" # no information available for this
        else:
            percentage = 100 * obs / total
            return f"{obs}/{total} ({int(percentage)}%)"
        

    def frequency_for_target_disease(self, disease: OntologyClass202) -> str:
        exc = self._d_to_excluded[disease]
        obs = self._d_to_observed[disease]
        total = exc + obs
        if total == 0:
            return "n/a" # no information available for this
        elif obs == 1:
            return f"observed"
        else:
            return "excluded"
        
    def __str__(self):
        items = list()
        for d in self._disease_set:
            items.append(f"{d.id}-{self.frequency_for_disease(d)}")
        return ";".join(items)

    def get_maximum_frequency(self):
        """
        We sort with a heuristic that rewards at least one disease with a high frequency AND an overall high number of observed counts.
        """
        frequencies = list() ## here we do not care about the actual order
        for k, v in self._d_to_observed.items():
            if v == 0:
                frequencies.append(0)
            else:
                exc = self._d_to_excluded.get(k, 0)
                obs = self._d_to_observed.get(k, 0)
                total = exc + obs
                frequencies.append(obs/total)
        if len(frequencies) == 0:
            return 0
        return max(frequencies)
    
    def get_weighted_maximum_frequency(self):
        """
        Heuristic for sorting - maximum frequency times toit
        """
        total = self.get_total() ## total number of observations
        max_f = self.get_maximum_frequency()
        return total * max_f



class DiseaseSpecificHpoCounter:

    def __init__(self, 
                 ppkt_list: typing.List[PPKt.Phenopacket],
                 target_ppkt: PPKt.Phenopacket = None,
                 hpo: hpotk.MinimalOntology = None) -> None:
        """
        :param ppkt_list: List of Phenopackets we wish to display as a table of HPO term counts
        :type ppkt_list: typing.list[PPKt.Phenopacket]
        :target_ppkt: Phenopacket of the individual that we wish to compare with the cohort that is represented in ppkt_list. Optional
        :type target_ppkt: typing.Optional[PPKt.Phenopacket]
        :param hpo: Reference to HPO ontology object (if nulll, will be created in constructor)
        :type hpo: hpotk.MinimalOntology
        """
        v202_ppkt = [Phenopacket202.from_message(ppkt) for ppkt in ppkt_list]
        if hpo is None:
            parser = HpoParser()
            self._hpo = parser.get_ontology()
        else:
            self._hpo = hpo
        disease_dict = defaultdict(list)
        for ppkt in v202_ppkt:
            if len(ppkt.diseases) != 1:
                raise ValueError(f"This class does not support visualization of phenopackets with more than one disease diagnosis")
            disease_term = ppkt.diseases[0]
            disease_dict[disease_term.term].append(ppkt)
        if target_ppkt is not None:
            ## We want to show the target as a separate column.
            ## use this term as a marker, it will not be displayed
            oclzz = OntologyClass202(id=TARGET_DISEASE_ID, label=target_ppkt.id) 
            disease_dict[oclzz].append(target_ppkt)
        hpo_to_counter = dict()
        self._hpo_term_ids_for_display = set()
        warn_terms = set() ## to avoid making the same error message multiple times
        # The following for loop extracts data for each disease one at a time.
        for disease_term, ppkt_list in disease_dict.items():
            for ppkt in ppkt_list:
                # We count not only explicitly annotated terms but also the ancestor of observed terms
                # and descendents of excluded terms.
                # Note that we keep track of explicitly annotated terms and these are the only ones we show in the output table
                observed_with_ancestors = set()
                excluded_with_descendants = set()
                for pf in ppkt.phenotypic_features:
                    oclzz = pf.type
                    hpo_term = self._hpo.get_term(oclzz.id)
                    if hpo_term.identifier.value != oclzz.id :
                        if hpo_term.identifier.value not in warn_terms:
                            warn_terms.add(hpo_term.identifier.value)
                            print("############# WARNING #############")
                            print(f"Use of outdated id {oclzz.id} ({oclzz.label}). Replacing with {hpo_term.identifier.value}.")
                            print("###################################") 
                        oclzz = OntologyClass202(id=hpo_term.identifier.value, label=hpo_term.name)
                    hpo_id = oclzz.id
                    self._hpo_term_ids_for_display.add(hpo_id)
                    if pf.excluded:
                        desc_set = self._hpo.graph.get_descendants(hpo_id, include_source=True)
                        excluded_with_descendants.update(desc_set)
                    else:
                        ancs_set = self._hpo.graph.get_ancestors(hpo_id, include_source=True)
                        observed_with_ancestors.update(ancs_set)
                for hpo_id in observed_with_ancestors:
                    hpo_label = self._hpo.get_term_name(hpo_id)
                    oclzz = OntologyClass202(id=hpo_id, label=hpo_label)
                    if oclzz not in hpo_to_counter:
                        hpo_to_counter[oclzz] = HpoCohortCount(hpo=oclzz)
                    hpo_to_counter.get(oclzz).increment_observed(disease_term)
                for hpo_id in excluded_with_descendants:
                    hpo_label = self._hpo.get_term_name(hpo_id)
                    oclzz = OntologyClass202(id=hpo_id, label=hpo_label)
                    if oclzz not in hpo_to_counter:
                        hpo_to_counter[oclzz] = HpoCohortCount(hpo=oclzz)
                    hpo_to_counter.get(oclzz).increment_excluded(disease_term)
        ## arrange the diseases according to number of annotated phenopackets
        disease_tuple_list =  [(k,v) for k, v in sorted(disease_dict.items(), key=lambda item: len(item[1]), reverse=True)]
        ## sort the HPO terms according to the overall frequency.
        self._disease_list = [x[0] for x in disease_tuple_list]
        hpo_to_counter_list = list(hpo_to_counter.values())
        self._hpo_to_counter_list = sorted(hpo_to_counter_list, key=lambda x: x.get_maximum_frequency(), reverse=True)


    def to_data_frame(self) -> pd.DataFrame:
        disease_labels = [d.label for d in self._disease_list]
        items = list()
        for hpo2c in self._hpo_to_counter_list:
            hpo_term = hpo2c.hpo
            if hpo_term.id.value not in self._hpo_term_ids_for_display:
                continue ## these will be the inferrence ancestors classes that are not used for explicitly for annotation, we want to skip them
            d = dict()
            d["HPO"] = hpo2c.hpo_display
            for disease in self._disease_list:
                if disease.id == TARGET_DISEASE_ID:
                    d[disease.label] = hpo2c.frequency_for_target_disease(disease)
                else:
                    d[disease.label] = hpo2c.frequency_for_disease(disease)
            items.append(d)
        df = pd.DataFrame(items)
        df_reset = df.reset_index(drop=True) # the index is irrelevant
        return df_reset

        
        

        
