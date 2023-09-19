from .simple_patient import SimplePatient
import pandas as pd
from .hpo_category import HpoCategorySet
from hpotk.model import TermId
from collections import defaultdict

ALL_ROOT = TermId.from_curie("HP:0000001")
PHENOTYPIC_ABNORMALITY_ROOT = TermId.from_curie("HP:0000118")



class DetailedSupplTable:
    """
    This class intends to facilitate the creation of a detailed supplemental tabular file with the phenotypic findings for
    an entire cohort. Each attribute (id, sex, age, HPO terms) are shown on rows, and the individuals who make up the cohort
    are shown as columns.
    """

    def __init__(self, patient_d, hp_ontology) -> None:
        """
        :param patient_d: dictionary of patients to display
        :type patient_d: map with key string and value SimplePatient
        """
        if not isinstance(patient_d, dict):
            raise ValueError(f"patient_d argument must be dictionary but was {type(patient_d)}")
        my_simple_patient_d = defaultdict(SimplePatient)
        for k, v in patient_d.items():
            if str(type(v)) != "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":
                my_simple_patient_d[k] = SimplePatient(ga4gh_phenopacket=v)
            else:
                raise ValueError(f"patient_d values must be GA4GH Phenopackets but was {type(v)}")
        self._patient_d = patient_d  # GA4GH phenopackets 
        self._simple_patient_d = my_simple_patient_d # SimplePatients
        self._hp_ontology = hp_ontology
        self._total_counts = defaultdict(int)
        self._total_counts_propagated = defaultdict(int)
        sex_d = defaultdict(int)
        var_d = defaultdict(int)
        for pat_id, pat in self._simple_patient_d.items():
            sex_d[pat.get_sex()] += 1
            hpo_terms = pat.get_observed_hpo_d()
            anc_set = set() # graph with ancestors induced by all terms of the patient
            for hp_id in hpo_terms.keys():
                # key is a string such as HP:0001234, value is an HpTerm object
                # we need to convert it to an object from hpo-toolkit because get_ancestors returns HpTerm objects
                hp_termid = TermId.from_curie(hp_id)
                ancs = self._hp_ontology.get_ancestors(hp_termid)
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


    def _get_table(self, counts_d):
        """
        Get counts of terms without annotation propagation or thresholding
        """
        rows = []
        N = self._n_patients
        for hpid, total_count in counts_d.items():
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


    
    def get_table_direct_annotations(self):
        """
        Get counts of terms without annotation propagation or thresholding
        """
        return self._get_table(self._total_counts)
    

    def get_table_with_propagated_counts(self):
        """
        Get counts of terms without annotation propagation or thresholding
        """
        return self._get_table(self._total_counts_propagated)
    
    @staticmethod
    def _get_counts(hpo_term_id:str, counts_d:dict):
        M = len(counts_d)
        N = sum([1 for x in counts_d.values if x.contains_observed_term_id(hpo_term_id)])
        return N, M
    

    def get_html_table_by_pmid(self):
        by_pmid_d = defaultdict(list)
        all_observed_hpo = defaultdict(int) # HPO ids observed in our cohort
        for pat in self._simple_patient_d.values():
            for hpo_term_id in pat.get_observed_hpo_d.values():
                all_observed_hpo[hpo_term_id] += 1
            if pat.has_pmid():
                by_pmid_d[pat.get_pmid()] = pat 
            else:
                by_pmid_d["n/a"] = pat 
        sorted_pmids = sorted(by_pmid_d.items(), key=lambda x:x[1], reverse=True) # sort by values
        sorted_hpos = sorted(all_observed_hpo.items(), key=lambda x:x[1], reverse=True)
        table_items = []
        table_items.append('<table style="border: 2px solid black;">\n')
        table_items.append(f'<caption>{capt}</caption>\n')
        table_items.append("<tr><th>HPO term</th>\n")
        middle = []
        for pmid in sorted_pmids:
            middle.append(f"<th>{pmid}</th>")
        middle_txt = "".join(middle)
        header = f"<tr><th>HPO term</th>{middle_txt}</tr>"
        for hpo_term_id in sorted_hpos:
            line_items = []
            line_items.append(f"<tr><td>{hpo_term_id}</td>")
            for pmid in sorted_pmids:
                counts_d = by_pmid_d.get(pmid)
                N, M = DetailedSupplTable._get_counts(hpo_term_id=hpo_term_id, counts_d=counts_d)
                cell_contents = f"{N}/{M} ({100*N/M:.1f}%)"
                line_items.append(cell_contents)
            line_items.append("</tr>\n")
            table_items.append("".join(line_items))
        table_items.append('</table>\n') # close table content
        return "\n".join(table_items)
        

            
        
        
        
