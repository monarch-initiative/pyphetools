import hpotk
import os
from typing import Dict
from .hpo_cr import HpoConceptRecognizer
from .hpo_exact_cr import HpoExactConceptRecognizer

HPO_JSON_URL = "http://purl.obolibrary.org/obo/hp/hp.json"

PHENOTYPE_ROOT = "HP:0000118"


class HpoParser:
    """
    Class to retrieve and parse the HPO JSON file using the HPO-Toolkit

    Users probably will want to pass the path to the hp.json file, but if not, the hp.json file
    will be downloadede each time the constructor is run

    :param hpo_json_file: path to the hp.json file
    :type hpo_json_file: str, optional
    """

    def __init__(self, hpo_json_file:str=None):
        if hpo_json_file is not None:
            if not os.path.isfile(hpo_json_file):
                raise FileNotFoundError(f"Could not find hp.json file at {hpo_json_file}")
            self._ontology = hpotk.load_ontology(hpo_json_file)
        else:
            self._ontology = hpotk.load_ontology(HPO_JSON_URL)

    def get_ontology(self):
        """
        :returns: a reference to the HPO
        :rtype: hpotk.Ontology
        """
        return self._ontology

    def get_label_to_id_map(self):
        """
        Create a map from a lower case version of HPO labels to the corresponding HPO id
        only include terms that are descendents of PHENOTYPE_ROOT

        :returns: a map from lower-case HPO term labels to HPO ids
        :rtype: Dict[str,str]
        """
        label_to_id_d = {}
        for t in self._ontology.terms:
            if t.is_obsolete:
                continue
            hpo_id = t.identifier.value
            if not self._ontology.graph.is_ancestor_of(PHENOTYPE_ROOT, hpo_id):
                continue
            label_to_id_d[t.name.lower()] = hpo_id
            # Add the labels of the synonyms
            if t.synonyms is not None and len(t.synonyms) > 0:
                for s in t.synonyms:
                    lc_syn = s.name.lower()
                    # only take synonyms with length at least 5 to avoid spurious matches
                    if len(lc_syn) > 4:
                        label_to_id_d[lc_syn] = hpo_id
        return label_to_id_d

    def get_id_to_label_map(self):
        """
        :returns: a map from HPO term ids to HPO labels
        :rtype: Dict[str,str]
        """
        id_to_label_d = {}
        for t in self._ontology.terms:
            if t.is_obsolete:
                continue
            id_to_label_d[t.identifier.value] = t.name
        return id_to_label_d

    def get_hpo_concept_recognizer(self) -> HpoConceptRecognizer:
        return HpoExactConceptRecognizer(label_to_id=self.get_label_to_id_map(),
                                         id_to_primary_label=self.get_id_to_label_map(),
                                         ontology=self.get_ontology())

    def get_version(self):
        return self._ontology.version.__str__()
