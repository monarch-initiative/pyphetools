from collections import defaultdict

import pandas as pd
from hpotk.model import TermId

from .hpo_category import HpoCategorySet

ALL_ROOT = TermId.from_curie("HP:0000001")
PHENOTYPIC_ABNORMALITY_ROOT = TermId.from_curie("HP:0000118")


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
        self._total_counts_propagated = defaultdict(int)
        self._focus_counts_propagated = defaultdict(int)
        self._non_focus_counts_propagated = defaultdict(int)
        self._n_patients = len(patient_d)

        sex_d = defaultdict(int)
        var_d = defaultdict(int)

        for pat_id, pat in self._patient_d.items():
            sex_d[pat.get_sex()] += 1
            hpo_terms = pat.get_observed_hpo_d()
            anc_set = set()  # graph with ancestors induced by all terms of the patient
            for hp_id in hpo_terms.keys():
                # key is a string such as HP:0001234, value is an HpTerm object
                # we need to convert it to an object from hpo-toolkit because get_ancestors returns HpTerm objects
                hp_termid = TermId.from_curie(hp_id)
                ancs = self._ontology.graph.get_ancestors(hp_termid)
                anc_set.add(hp_termid)
                anc_set.update(ancs)
                if pat_id in focus_id:
                    self._focus_counts[hp_id] += 1
                else:
                    self._non_focus_counts[hp_id] += 1
                self._total_counts[hp_id] += 1
            for hp_id in anc_set:
                if hp_id == ALL_ROOT or hp_id == PHENOTYPIC_ABNORMALITY_ROOT:
                    continue
                if pat_id in focus_id:
                    self._focus_counts_propagated[hp_id.value] += 1
                else:
                    self._non_focus_counts_propagated[hp_id.value] += 1
                self._total_counts_propagated[hp_id.value] += 1
            variant_d = pat.get_variant_list()
            for var in variant_d:
                var_d[var] += 1

            # TODO figure out what to do with biallelic
        self._hpo_category_set = HpoCategorySet(ontology=ontology)

    def get_category(self, termid):
        # TODO figure out what to do with biallelic
        cat = self._hpo_category_set.get_category(termid=termid)
        if cat == "not_found":
            print(f"could not find category for {termid}")
        return cat

    def get_simple_table(self):
        """
        Get counts of terms within annotation propagation or thresholding
        """
        rows = []
        N = self._n_patients
        for hpid, total_count in self._total_counts.items():
            total_per = 100 * total_count / N
            total_s = f"{total_count}/{N} ({total_per:.1f}%)"
            hpterm = self._ontology.get_term(hpid)
            cat = self.get_category(termid=hpid)
            focus_count = self._focus_counts.get(hpid, 0)
            other_count = self._non_focus_counts.get(hpid, 0)
            d = {'category': cat, 'term': hpterm.name, 'HP:id': hpid, 'focus': focus_count, 'other': other_count,
                 'total': total_s, 'total_count': total_count}
            rows.append(d)
        df = pd.DataFrame(rows)
        df.set_index('category', inplace=True)
        return df.sort_values(['category', 'total_count'], ascending=[True, False])

    def get_thresholded_table(self, min_proportion: float = None, min_count: int = None):
        if min_count is None and min_proportion is None:
            raise ValueError("One of the arguments min_proportion and min_count must be provided")
        elif min_count is not None and min_proportion is not None:
            raise ValueError("Not more than one of the arguments min_proportion and min_count must be provided")
        elif min_proportion is not None:
            min_count = round(self._n_patients * min_proportion)
        print(f"Output terms with at least {min_count} counts")
        N = self._n_patients
        rows = []
        for hpid, total_count in self._total_counts_propagated.items():
            if total_count < min_count:
                continue
            total_per = 100 * total_count / N
            total_s = f"{total_count}/{N} ({total_per:.1f}%)"
            hpterm = self._ontology.get_term(hpid)
            cat = self.get_category(termid=hpid)
            focus_count = self._focus_counts_propagated.get(hpid, 0)
            other_count = self._non_focus_counts_propagated.get(hpid, 0)
            d = {'category': cat, 'term': hpterm.name, 'HP:id': hpid, 'focus': focus_count, 'other': other_count,
                 'total': total_s, 'total_count': total_count}
            rows.append(d)
        if len(rows) == 0:
            return pd.DataFrame(columns=['category', 'total_count'])
        df = pd.DataFrame(rows)
        df.set_index('category', inplace=True)
        return df.sort_values(['category', 'total_count'], ascending=[True, False])
