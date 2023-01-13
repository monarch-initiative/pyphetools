from .simple_patient import SimplePatient
import pandas as pd
from .hpo_category import HpoCategorySet
from hpotk.model import TermId
from hpotk.algorithm import get_ancestors
from collections import defaultdict
from hpotk.algorithm import exists_path

ALL_ROOT = TermId.from_curie("HP:0000001")
PHENOTYPIC_ABNORMALITY_ROOT = TermId.from_curie("HP:0000118")



class DetailedSupplTable:
    """
    This class intends to facilitate the creation of a detailed supplemental Excel file with the phenotypic findings for
    an entire cohort. Each attribute (id, sex, age, HPO terms) are shown on rows, and the individuals who make up the cohort
    are shown as columns.
    """

    def __init__(self, patient_d, hp_ontology) -> None:
        if not isinstance(patient_d, dict):
            raise ValueError(f"patient_d argument must be dictionary but was {type(patient_d)}")
        self._patient_d = patient_d
        self._hp_ontology = hp_ontology
        self._total_counts = defaultdict(int)
        sex_d = defaultdict(int)
        var_d = defaultdict(int)
        for pat_id, pat in self._patient_d.items():
            sex_d[pat.get_sex()] += 1
            hpo_terms = pat.get_observed_hpo_d()
            anc_set = set() # graph with ancestors induced by all terms of the patient
            for hp_id in hpo_terms.keys():
                # key is a string such as HP:0001234, value is an HpTerm object
                # we need to convert it to an object from hpo-toolkit because get_ancestors returns HpTerm objects
                hp_termid = TermId.from_curie(hp_id)
                ancs = get_ancestors(self._hp_ontology,hp_termid)
                anc_set.add(hp_termid)
                anc_set.update(ancs)
                self._total_counts[hp_id] += 1
            for hp_id in anc_set:
                if hp_id == ALL_ROOT or hp_id == PHENOTYPIC_ABNORMALITY_ROOT:
                    continue
                else:
                    self._total_counts_propagated[hp_id.value] += 1
            variant_d = pat.get_variant_d()
            for var in variant_d.keys():
                var_d[var] += 1

            # TODO figure out what to do with biallelic
        self._hpo_category_set = HpoCategorySet(ontology=hp_ontology)


    def get_table(self):
        """
        Get counts of terms within annotation propagation or thresholding
        """
        rows = []
        N = self._n_patients
        for hpid, total_count in self._total_counts.items():
            total_per = 100*total_count/N
            total_s = f"{total_count}/{N} ({total_per:.1f}%)"
            hpterm = self._ontology.get_term(hpid)
            cat = self.get_category(termid=hpid)
            focus_count = self._focus_counts.get(hpid, 0)
            other_count = self._non_focus_counts.get(hpid, 0)
            d = {'category': cat, 'term': hpterm.name, 'HP:id': hpid, 'focus' : focus_count, 'other': other_count, 'total': total_s, 'total_count': total_count}
            rows.append(d)
        df = pd.DataFrame(rows)
        df.set_index('category', inplace=True)
        return df.sort_values(['category', 'total_count'], ascending=[True, False])