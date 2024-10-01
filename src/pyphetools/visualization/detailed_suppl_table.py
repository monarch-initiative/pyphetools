from .simple_patient import SimplePatient
from ..creation.hpo_parser import HpoParser
import pandas as pd
import phenopackets as PPKt
import typing
from .hpo_category import HpoCategorySet
from hpotk.model import TermId
from collections import defaultdict
import hpotk
from enum import Enum


ALL_ROOT = TermId.from_curie("HP:0000001")
PHENOTYPIC_ABNORMALITY_ROOT = TermId.from_curie("HP:0000118")

class HpoStatus(Enum):
    OBSERVED = 1, "observed"
    EXCLUDED = 2, "excluded"
    NOT_AVAILABLE = 3, "na"


class HpoTableCell:
    """
    Represents one cell of the detailed table
    """
    def __init__(self, 
                 hpo_term_id:hpotk.TermId,
                 status: HpoStatus
                 ) -> None:
        self._hpo_id = hpo_term_id
        self._status = status

    def to_cell(self):
        return self._status.value
    
    def to_cell_pm(self):
        """
        Alternative plus-minus (pm) notation
        """
        if self._status == HpoStatus.OBSERVED:
            return "+"
        elif self._status == HpoStatus.EXCLUDED:
            return "-"
        else:
            return "na"



class DetailedSupplTable:
    """
    This class intends to facilitate the creation of a detailed supplemental tabular file with the phenotypic findings for
    an entire cohort. Each attribute (id, sex, age, HPO terms) are shown on rows, and the individuals who make up the cohort
    are shown as columns.
    """

    def __init__(self, 
                 patient_list: typing.List[PPKt.Phenopacket], 
                 hp_json:str=None) -> None:
        """
        :param patient_d: dictionary of patients to display
        :type patient_d: map with key string and value SimplePatient
        """
        parser = HpoParser(hpo_json_file=hp_json)
        hp_ontology = parser.get_ontology()
        if not isinstance(patient_list, list):
            raise ValueError(f"patient_list argument must be dictionary but was {type(patient_list)}")
        self._simple_patient_list = list()
        for v in patient_list:
            if str(type(v)) == "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":
                self._simple_patient_list.append(SimplePatient(ga4gh_phenopacket=v))
            else:
                raise ValueError(f"patient_d values must be GA4GH Phenopackets but was {type(v)}")
        self._hp_ontology = hp_ontology
        self._total_counts = defaultdict(int)
        self._total_counts_propagated = defaultdict(int)
        sex_d = defaultdict(int)
        var_d = defaultdict(int)
        for pat in self._simple_patient_list:
            sex_d[pat.get_sex()] += 1
            hpo_terms = pat.get_observed_hpo_d()
            anc_set = set() # graph with ancestors induced by all terms of the patient
            for hp_id in hpo_terms.keys():
                # key is a string such as HP:0001234, value is an HpTerm object
                # we need to convert it to an object from hpo-toolkit because get_ancestors returns HpTerm objects
                hp_termid = TermId.from_curie(hp_id)
                if not self._hp_ontology.graph.is_descendant_of(hp_termid, PHENOTYPIC_ABNORMALITY_ROOT):
                    continue # do not count terms that are not phenotypes
                ancs = self._hp_ontology.graph.get_ancestors(hp_termid)
                anc_set.add(hp_termid)
                anc_set.update(ancs)
                self._total_counts[hp_id] += 1
            for hp_id in anc_set:
                if hp_id == ALL_ROOT or hp_id == PHENOTYPIC_ABNORMALITY_ROOT:
                    continue
                else:
                    self._total_counts_propagated[hp_id.value] += 1
            variants = pat.get_variant_list()
            for var in variants:
                var_d[var] += 1
        self._hpo_category_set = HpoCategorySet(ontology=hp_ontology)

    def _calculate_table(self, patient_list: typing.List[PPKt.Phenopacket], ) -> typing.List[typing.List[str]]:
        for pat in self._simple_patient_list:
            hpo_terms = pat.get_observed_hpo_d()
            anc_set = set() # graph with ancestors induced by all terms of the patient



    def _get_table(self, counts_d):
        """
        Get counts of terms without annotation propagation or thresholding
        """
        rows = []
        N = len(self._patient_d)
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
        N = 0
        for _, v in counts_d.items():
            if v.contains_observed_term_id(hpo_term_id):
                N += 1
        return N, M
    
    @staticmethod
    def _get_counts_dict(pat_list):
        counts_d = defaultdict(int)
        for pat in pat_list:
            observed_hpo = pat.get_observed_hpo_d()
            for hpo_term_id in observed_hpo.keys():
                counts_d[hpo_term_id] += 1
        return counts_d   
    

    def get_html_table_by_pmid(self, min_count=0):
        """
        :param min_count: minimum count to be displayed ion the table (by default, all terms are displayed)
        :type min_count: int
        """
        by_pmid_d = defaultdict(list)
        all_observed_hpo = defaultdict(int) # HPO ids observed in our cohort
        hpo_id_to_display_d = defaultdict()
        for pat in self._simple_patient_list:
            observed_hpo_d = pat.get_observed_hpo_d()
            for hpo_term in observed_hpo_d.values():
                hpo_term_id = hpo_term.id
                all_observed_hpo[hpo_term_id] += 1
                hpo_id_to_display_d[hpo_term_id] = hpo_term
            if pat.has_pmid():
                by_pmid_d[pat.get_pmid()].append(pat) 
            else:
                by_pmid_d["n/a"].append(pat) 
        sorted_pmids = sorted(by_pmid_d.items(), key=lambda x:len(x[1]), reverse=True) # sort by values
        sorted_pmids = [ x[0] for x  in sorted_pmids]
        sorted_hpos = sorted(all_observed_hpo.items(), key=lambda x:x[1], reverse=True)
        sorted_hpos = [ x[0] for x  in sorted_hpos if x[1] > min_count]
        table_items = []
        table_items.append('<table style="border: 2px solid black;">\n')
        middle = []
        for pmid in sorted_pmids:
            middle.append(f"<th>{pmid}</th>")
        middle_txt = "".join(middle)
        header = f"<tr><th>HPO term</th>{middle_txt}</tr>"
        table_items.append(header)
        for hpo_term_id in sorted_hpos:
            hpo_term = hpo_id_to_display_d.get(hpo_term_id)
            line_items = []
            line_items.append(f"<tr><td>{hpo_term}</td>")
            for pmid in sorted_pmids:
                simple_pat_list = by_pmid_d.get(pmid)
                counts_d = DetailedSupplTable._get_counts_dict(simple_pat_list)
                M = len(simple_pat_list)
                N = counts_d.get(hpo_term_id, 0)
                cell_contents = f"{N}/{M} ({100*N/M:.1f}%)"
                line_items.append(f"<td>{cell_contents}</td>")
            line_items.append("</tr>\n")
            table_items.append("".join(line_items))
        table_items.append('</table>\n') # close table content
        return "\n".join(table_items)
        

            
        
        
        
