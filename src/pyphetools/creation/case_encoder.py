from google.protobuf.json_format import MessageToJson
import os
import pandas as pd
import phenopackets as PPKt
import re
from typing import Set
from collections import defaultdict
from .column_mapper import ColumnMapper
from .constants import Constants
from .disease import Disease
from .hp_term import HpTerm
from .hpo_cr import HpoConceptRecognizer
from .individual import Individual
from .simple_column_mapper import SimpleColumnMapper
from .variant import Variant

ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"


class CaseEncoder:
    """Encode a single case report in GA4GH Phenopacket format.

    This class should be used to encode a single case report; it outputs an Individual object that can be converted
    into a GA4GH phenopacket.

    :param hpo_cr: HpoConceptRecognizer for text mining
    :type hpo_cr: pyphetools.creation.HpoConceptRecognizer
    :param pmid: PubMed identifier of this case report
    :type pmid: str
    :param individual_id: Application specific individual identifier
    :type individual_id: str
    :param metadata: GA4GH MetaData object
    :type metadata: phenopackets.MetaData
    :param  age_at_last_exam: An ISO8601 string (e.g., P42Y2M) representing the age of the individual
    :type age_at_last_exam: str, optional
    :param sex: A string such as "male" or "FEMALE"
    :type sex: str
    :param disease: an object with the identifier and name of the disease diagnosis
    :type disease: Disease, optional
    """

    def __init__(self,
                hpo_cr: HpoConceptRecognizer,
                pmid: str,
                individual_id:str,
                metadata:PPKt.MetaData,
                age_at_last_exam:str=None,
                sex:str=None,
                disease:Disease=None) -> None:
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(
                f"concept_recognizer argument must be HpoConceptRecognizer but was {type(hpo_cr)}")
        self._hpo_concept_recognizer = hpo_cr
        if not pmid.startswith("PMID:"):
            raise ValueError(f"Malformed pmid argument ({pmid}). Must start with PMID:")
        if age_at_last_exam is not None:
            match = re.search(ISO8601_REGEX, age_at_last_exam)
            if match:
                self._age_at_last_examination = age_at_last_exam
            else:
                raise ValueError(f"Could not parse {age_at_last_exam} as ISO8601 period")
        else:
            self._age_at_last_examination = None
        self._seen_hpo_terms = set() # Use to prevent duplicate HP annotations
        if not isinstance(metadata, PPKt.MetaData):
            raise ValueError(f"metadata argument must be phenopackets.MetaData but was {type(metadata)}")
        self._metadata = metadata
        female_symbols = {"f", "girl", "female", "woman", "w"}
        male_symbols = {"f", "boy", "male", "man", "m"}
        if sex is None:
            sex_symbol = Constants.UNKOWN_SEX_SYMBOL
        elif sex.lower() in female_symbols:
            sex_symbol = Constants.FEMALE_SYMBOL
        elif sex.lower() in male_symbols:
            sex_symbol = Constants.MALE_SYMBOL
        else:
            print(f"Warning: did not recognize sex symbol \"{sex}\"")
            sex_symbol = Constants.UNKOWN_SEX_SYMBOL
        ontology = hpo_cr.get_hpo_ontology()
        if ontology is None:
            raise ValueError("ontology cannot be None")
        self._individual = Individual(individual_id=individual_id, sex=sex_symbol)
        if age_at_last_exam is not None:
            self._individual.set_age(age_at_last_exam)
        if disease is not None:
            self._individual.set_disease(disease=disease)
        if pmid is not None:
            self._individual.set_pmid(pmid=pmid)


    def add_vignette(self, vignette, custom_d=None, custom_age=None, false_positive=None, excluded_terms:Set[str]=None) -> pd.DataFrame:
        """Add a description of a clinical encouter for text mining

        This method uses simple text mining to extract terms from the vignette. The optional custom_d argument can be
        used for HPO terms that are not mined by the text miner (users should use the preview to check the performance
        of the default miner and add terms as needed/desired). Note that HpTerms are added to the CaseEncoder object; these
        terms are also returned as a pandas DataFrame for checking.

        :param vignette: A free text description of a clinical encounter (we will use text mining to extract HPO terms)
        :type vignette: str
        :param custom_d: A dictionary of strings that correspond to HPO terms
        :type custom_d: dict
        :param custom_age: Age for the features in the current vignette
        :type custom_age: str
        :param false_positive: a set of strings that are omitted from text mining to avoid false positive results
        :type false_positive: set
        :param excluded_terms: similar to custom_d but for terms that are explicitly excluded in the vignette
        :type excluded_terms: Set[str]
        :returns: dataframe of (unique, alphabetically sorted) HpTerm objects with observed or excluded HPO terms
        :rtype: pd.DataFrame
        """
        if excluded_terms is None:
            excluded_terms = set()
        elif not isinstance(excluded_terms, set):
            raise ValueError(f"excluded_terms argument must be a set with HPO labels that have been explicitly excluded; but we got {type(excluded_terms)}")
        if false_positive is None:
            false_positive = set()
        elif not isinstance(false_positive, set):
            raise ValueError(f"false_positive argument must be a set with HPO labels that have been explicitly excluded; but we got {type(false_positive)}")
        if custom_d is None:
            custom_d = {}
        # replace new lines and multiple consecutive spaces with a single space
        text = re.sub(r'\s+', ' ', vignette.replace('\n', ' '))
        for fp in false_positive:
            text = text.replace(fp, " ")
        # results will be a list with HpTerm elements
        results = self._hpo_concept_recognizer.parse_cell(cell_contents=text, custom_d=custom_d)
        if custom_age is not None:
            current_age = custom_age
        elif self._age_at_last_examination is not None:
            current_age = self._age_at_last_examination
        else:
            current_age = Constants.NOT_PROVIDED
        for term in results:
            if term in self._seen_hpo_terms:
                continue
            else:
                self._seen_hpo_terms.add(term)
            if term.label in excluded_terms:
                term.excluded()
            term.set_onset(current_age)
            self._individual.add_hpo_term(term)
        return HpTerm.term_list_to_dataframe(results)

    def add_term(self, label=None, hpo_id=None, excluded=False, custom_age=None):
        """
        Add a single HPO term to the current case.
        :param label: Label of the HPO term
        :type label: str
        :param hpo_id: identifier of the term, e.g. HP:0001234
        :type hpo_id: str
        :param excluded: True iff the abnormally was explicitly excludeds
        :type excluded: bool
        :param custom_age: an ISO 8601 string representing the age of onset of the abnormality
        :type custom_age: str
        """
        if label is not None:
            results = self._hpo_concept_recognizer.parse_cell(cell_contents=label, custom_d={})
            if len(results) != 1:
                raise ValueError(f"Malformed label \"{label}\" we got {len(results)} results")
            hpo_term = results[0]
            hpo_term._observed = not excluded
            if custom_age is not None:
                hpo_term.set_onset(custom_age)
                self._individual.add_hpo_term(hpo_term)
            elif self._age_at_last_examination is not None:
                hpo_term.set_onset(self._age_at_last_examination)
                self._individual.add_hpo_term(hpo_term)
            else:
                hpo_term.set_onset(Constants.NOT_PROVIDED)
                self._individual.add_hpo_term(hpo_term)
            return HpTerm.term_list_to_dataframe([hpo_term])
        elif hpo_id is not None:
            hpo_term = self._hpo_concept_recognizer.get_term_from_id(hpo_id)
            if excluded:
                hpo_term._observed = not excluded
            if custom_age is not None:
                hpo_term.set_onset(custom_age)
                self._individual.add_hpo_term(hpo_term)
            elif self._age_at_last_examination is not None:
                hpo_term.set_onset(self._age_at_last_examination)
                self._individual.add_hpo_term(hpo_term)
            else:
                hpo_term.set_onset(Constants.NOT_PROVIDED)
                self._individual.add_hpo_term(hpo_term)
            return HpTerm.term_list_to_dataframe([hpo_term])
        else:
            return ValueError("Must call function with non-None value for either id or label argument")


    def add_variant_or_interpretation(self, variant_or_variantInterpretation):
        """
        :param variant_or_variantInterpretation: A presumed pathogenic variant observed in the current individual
        :type variant_or_variantInterpretation: Union[Variant, phenopackets.VariantInterpretation]
        """
        if isinstance(variant_or_variantInterpretation, Variant):
            interpretation = variant_or_variantInterpretation.to_ga4gh_variant_interpretation()
            self._individual.add_variant(interpretation)
        elif isinstance(variant_or_variantInterpretation, PPKt.VariantInterpretation):
            self._individual.add_variant(variant_or_variantInterpretation)
        else:
            raise ValueError(f"variant argument must be pyphetools Variant or GA4GH \
                phenopackets.VariantInterpretation but was {type(variant_or_variantInterpretation)}")

    def initialize_simple_column_maps(self, column_name_to_hpo_label_map, observed, excluded, non_measured=None):
        if observed is None or excluded is None:
            raise ValueError("Symbols for observed (e.g., +, Y, yes) and excluded (e.g., -, N, no) required")
        if not isinstance(column_name_to_hpo_label_map, dict):
            raise ValueError("column_name_to_hpo_label_map must be a dict with column to HPO label mappings")
        simple_mapper_d = defaultdict(ColumnMapper)
        for column_name, hpo_label in column_name_to_hpo_label_map.items():
            hp_term = self._hpo_concept_recognizer.get_term_from_label(hpo_label)
            mpr = SimpleColumnMapper(hpo_id=hp_term.id, hpo_label=hp_term.label, observed=observed, excluded=None,non_measured=non_measured)
            simple_mapper_d[column_name] = mpr
        return simple_mapper_d

    def get_hpo_term_dict(self):
        return self._annotations

    def get_individual(self)-> Individual:
        """
        :return: the pyphetools Individual object corresponding to the current case report
        :rtype: Individual
        """
        return self._individual

    def get_phenopacket(self):
        """
        :return: the GA4GH phenopacket corresponding to the current case report
        :rtype: PPKt.Phenopacket
        """
        individual = self.get_individual()
        pmid = individual.pmid
        phenopacket_id = pmid.replace(":", "_") + "_" + individual.id.replace(" ", "_").replace(":", "_")
        return individual.to_ga4gh_phenopacket(metadata=self._metadata, phenopacket_id=phenopacket_id)

    def output_phenopacket(self, outdir):
        """write a phenopacket to an output directory

        :param outdir: name of directory to write phenopackets
        :type outdir: str
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

