import re
import os
from typing import List
from collections import defaultdict
from .hp_term import HpTerm
from .hpo_cr import HpoConceptRecognizer
from google.protobuf.json_format import MessageToJson
from .individual import Individual
import phenopackets



ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"





class CaseEncoder:
    
    
    def __init__(self, concept_recognizer, pmid, age_at_last_exam=None) -> None:
        if not isinstance(concept_recognizer, HpoConceptRecognizer):
            raise ValueError("concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._concept_recognizer = concept_recognizer
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

        self._annotations = defaultdict(list)


    def add_vignette(self, vignette, custom_d=None, custom_age=None, false_positive = [], excluded_terms = set()) -> List[HpTerm]:
        """
        false_positive: words or phrases that should not be parsed to HP terms
        """
        if custom_d is None:
            custom_d = {}
        # replace new lines and multiple consecutive spaces with a single space
        text = re.sub('\s+',' ',vignette.replace('\n', ' '))
        for fp in false_positive:
            text = text.replace(fp, " ")
        # results will be a list with HpTerm elements
        results =  self._concept_recognizer._parse_chunk(chunk=text, custom_d=custom_d)
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
        
    def add_term(self, label=None, id=None, excluded=False, custom_age=None):
        if label is not None:
            results =  self._concept_recognizer._parse_chunk(chunk=label, custom_d={})
            if len(results) != 1:
                raise ValueError(f"Malformed label {label}  we got {len(results)} results")
            hpo_term = results[0]
            hpo_term._observed = not excluded
            if custom_age is not None:
                self._annotations[custom_age].append(hpo_term)
            elif self._age_at_last_examination is not None:
                self._annotations[self._age_at_last_examination].append(hpo_term)
            else:
                self._annotations["N/A"].append(hpo_term)
            return HpTerm.term_list_to_dataframe([hpo_term])
        elif id is not None:
            hpo_term = self._concept_recognizer.get_term_from_id(id)
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


    def get_hpo_term_dict(self):
        return self._annotations

    def get_phenopacket(self, individual_id, metadata,  sex=None, age=None, disease_id=None, disease_label=None, variants=None):
        if not isinstance(variants, list):
            variants = [variants]
        individual = Individual(individual_id=individual_id, sex=sex, age=age, hpo_terms=self._annotations,
                       variant_list=variants, disease_id=disease_id, disease_label=disease_label)
        phenopacket_id = self._pmid.replace(":", "_") + "_" + individual.id.replace(" ", "_").replace(":", "_")
        return individual.to_ga4gh_phenopacket(metadata=metadata, phenopacket_id=phenopacket_id)
        

    def output_phenopacket(self, outdir, phenopacket):
        """_summary_

        Args:
            outdir (_type_): name of directory to write phenopackets
            individual_list (_type_, optional): List of individuals. If None, recreate
        """
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        phenopacket_id = phenopacket.id
        json_string = MessageToJson(phenopacket)
        fname = phenopacket_id.replace(" ", "_") + ".json"
        outpth = os.path.join(outdir, fname)
        with open(outpth, "wt") as fh:
            fh.write(json_string)
            print(f"Wrote phenopacket to {outpth}")