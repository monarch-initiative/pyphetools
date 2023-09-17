from google.protobuf.json_format import MessageToJson
import os
import phenopackets
import re
from typing import List
from collections import defaultdict
from .hp_term import HpTerm
from .hpo_cr import HpoConceptRecognizer
from .simple_column_mapper import SimpleColumnMapper
from .column_mapper import ColumnMapper

from .individual import Individual
from .variant import Variant

ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"


class CaseEncoder:
    """encode a single case report with HPO terms in Phenopacket format
    """

    def __init__(self, 
                 hpo_cr: HpoConceptRecognizer, 
                 pmid: str, 
                 individual_id:str, 
                 metadata:phenopackets.MetaData, 
                 age_at_last_exam=None, 
                 sex:str=None, 
                 age:str=None, 
                 disease_id:str=None, 
                 disease_label:str=None) -> None:
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(
                "concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._hpo_concept_recognizer = hpo_cr
        if not pmid.startswith("PMID:"):
            raise ValueError(f"Malformed pmid argument ({pmid}). Must start with PMID:")
        self._pmid = pmid
        if age_at_last_exam is not None:
            match = re.search(ISO8601_REGEX, age_at_last_exam)
            if match:
                self._age_at_last_examination = age_at_last_exam
            else:
                raise ValueError(f"Could not parse {age_at_last_exam} as ISO8601 period")
        else:
            self._age_at_last_examination = None
        self._seen_hpo_terms = set() # Use to prevent duplicate HP annotations
        self._annotations = defaultdict(list)
        self._individual_id = individual_id
        if not isinstance(metadata, phenopackets.MetaData):
            raise ValueError(f"metadata argument must be phenopackets.MetaData but was {type(metadata)}")
        self._metadata = metadata
        self._sex = sex
        self._age = age
        self._disease_id = disease_id
        self._disease_label = disease_label
        self._interpretations = []

    def add_vignette(self, vignette, custom_d=None, custom_age=None, false_positive=[], excluded_terms=set()) -> List[
        HpTerm]:
        """
        false_positive: words or phrases that should not be parsed to HP terms
        """
        if custom_d is None:
            custom_d = {}
        # replace new lines and multiple consecutive spaces with a single space
        text = re.sub(r'\s+', ' ', vignette.replace('\n', ' '))
        for fp in false_positive:
            text = text.replace(fp, " ")
        # results will be a list with HpTerm elements
        results = self._hpo_concept_recognizer.parse_cell(cell_contents=text, custom_d=custom_d)
        hpo_list = []
        for trm in results:
            if trm in self._seen_hpo_terms:
                continue
            else:
                self._seen_hpo_terms.add(trm)
            hpo_list.append(trm)
        if custom_age is not None:
            self._annotations[custom_age].extend(results)
        elif self._age_at_last_examination is not None:
            self._annotations[self._age_at_last_examination].extend(results)
        else:
            self._annotations["N/A"].extend(results)
        for r in results:
            if r.label in excluded_terms:
                r.excluded()
        return HpTerm.term_list_to_dataframe(results)

    def add_term(self, label=None, hpo_id=None, excluded=False, custom_age=None):
        if label is not None:
            results = self._hpo_concept_recognizer.parse_cell(cell_contents=label, custom_d={})
            if len(results) != 1:
                raise ValueError(f"Malformed label \"{label}\" we got {len(results)} results")
            hpo_term = results[0]
            hpo_term._observed = not excluded
            if custom_age is not None:
                self._annotations[custom_age].append(hpo_term)
            elif self._age_at_last_examination is not None:
                self._annotations[self._age_at_last_examination].append(hpo_term)
            else:
                self._annotations["N/A"].append(hpo_term)
            return HpTerm.term_list_to_dataframe([hpo_term])
        elif hpo_id is not None:
            hpo_term = self._hpo_concept_recognizer.get_term_from_id(hpo_id)
            if excluded:
                hpo_term._observed = not excluded
            if custom_age is not None:
                self._annotations[custom_age].append(hpo_term)
            elif self._age_at_last_examination is not None:
                self._annotations[self._age_at_last_examination].append(hpo_term)
            else:
                self._annotations["N/A"].append(hpo_term)
            return HpTerm.term_list_to_dataframe([hpo_term])
        else:
            return ValueError("Must call function with non-None value for either id or label argument")
        
        
    def add_variant_or_interpretation(self, variant):
        if isinstance(variant, Variant):
            self._interpretations.append(variant.to_ga4gh_variant_interpretation())
        elif isinstance(variant, phenopackets.VariantInterpretation):
            self._interpretations.append(variant)
        else:
            raise ValueError(f"variant argument must be pyphetools Variant or GA4GH \
                phenopackets.VariantInterpretation but was {type(variant)}")
            

    def initialize_simple_column_maps(self, column_name_to_hpo_label_map, observed, excluded, non_measured=None):
        if observed is None or excluded is None:
            raise ValueError("Symbols for observed (e.g., +, Y, yes) and excluded (e.g., -, N, no) required")
        if not isinstance(column_name_to_hpo_label_map, dict):
            raise ValueError("column_name_to_hpo_label_map must be a dict with column to HPO label mappings")
        simple_mapper_d = defaultdict(ColumnMapper)
        for column_name, hpo_label in column_name_to_hpo_label_map.items():
            hp_term = self._hpo_concept_recognizer.get_term_from_label(hpo_label)
            mpr = SimpleColumnMapper(hpo_id=hp_term.id, hpo_label=hp_term.label, observed=observed, excluded=None,
                                     non_measured=non_measured)
            simple_mapper_d[column_name] = mpr
        return simple_mapper_d

    def get_hpo_term_dict(self):
        return self._annotations

    def get_phenopacket(self):
        interpretations = self._interpretations
        if not isinstance(interpretations, list):
            interpretations = [interpretations]
        individual = Individual(individual_id=self._individual_id, 
                                sex=self._sex, 
                                age=self._age, 
                                hpo_terms=self._annotations,
                                pmid=self._pmid,
                                interpretation_list=self._interpretations, 
                                disease_id=self._disease_id, 
                                disease_label=self._disease_label)
        phenopacket_id = self._pmid.replace(":", "_") + "_" + individual.id.replace(" ", "_").replace(":", "_")
        return individual.to_ga4gh_phenopacket(metadata=self._metadata, phenopacket_id=phenopacket_id)

    def output_phenopacket(self, outdir):
        """write a phenopacket to an output directory

        Args:
            outdir (str): name of directory to write phenopackets
            phenopacket (Phenopacket): GA4GH Phenopacket object
        """
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        phenopacket = self.get_phenopacket()
        phenopacket_id = phenopacket.id
        json_string = MessageToJson(phenopacket)
        fname = phenopacket_id.replace(" ", "_") + ".json"
        outpth = os.path.join(outdir, fname)
        with open(outpth, "wt") as fh:
            fh.write(json_string)
            print(f"Wrote phenopacket to {outpth}")
