from .simple_patient import SimplePatient
import pandas as pd
from .hpo_category import HpoCategorySet
from hpotk.model import TermId
from collections import defaultdict
from hpotk.algorithm import exists_path

# typing.Union[GraphAware, OntologyGraph],
              #  source: CURIE_OR_TERM_ID,
               # destination: TermId) -> bo


class FocusCountTable:

    def __init__(self, patient_d, focus_id, ontology) -> None:
        if not isinstance(patient_d, dict):
            raise ValueError(f"patient_d argument must be dictionary but was {type(patient_d)}")
        self._patient_d = patient_d
        if isinstance(focus_id, str):
            self._focus_id_list = [focus_id]
        elif isinstance(focus_id, list):
            self._focus_id_list = focus_id
        else:
            raise ValueError(f"focus_id argument must be string or list of strings but was {type(focus_id)}")
        if len(self._focus_id_list) < 1:
            raise ValueError("Must provide at least one focus ID for FocusCountTable")
        self._ontology = ontology
        self._total_counts = defaultdict(int)
        self._focus_counts = defaultdict(int)
        self._non_focus_counts = defaultdict(int)
        self._n_patients = len(patient_d)
    
        sex_d = defaultdict(int)
        var_d = defaultdict(int)

        for pat_id, pat in self._patient_d.items():
            sex_d[pat.get_sex()] += 1
            hpo_terms = pat.get_observed_hpo_d()
            for hp_id in hpo_terms.keys():
                if pat_id in focus_id:
                    self._focus_counts[hp_id] += 1
                else:
                    self._non_focus_counts[hp_id] += 1
                self._total_counts[hp_id] += 1
            variant_d = pat.get_variant_d()
            for var in variant_d.keys():
                var_d[var] += 1
            # TODO figure out what to do with biallelic
    


    def get_category(self, termid):
        if termid in self._id_to_cat_d:
            return self._id_to_cat_d.get(termid)
        for cat, cat_hp_id in self._organ_d.items():
            if exists_path(self._ontology , termid, cat_hp_id):
                self._id_to_cat_d[cat_hp_id] = termid
                return cat
        print(f"Could not find category for {termid}")
        return "not_found"

    def get_simple_table(self):
        rows = []
        N = self._n_patients
        for hpid, total_count in self._total_counts.items():
            total_per = 100*total_count/N
            total_s = f"{total_count}/{N} ({total_per:.1f}%)"
            hpterm = self._ontology.get_term(hpid)
            focus_count = self._focus_counts.get(hpid, 0)
            other_count = self._non_focus_counts.get(hpid, 0)
            d = {'term': hpterm.name, 'HP:id': hpid, 'focus' : focus_count, 'other': other_count, 'total': total_s}
            rows.append(d)
        return pd.DataFrame(rows)




        
        