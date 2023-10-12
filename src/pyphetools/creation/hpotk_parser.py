import hpotk
import os
from typing import Dict
from .hpo_cr import HpoConceptRecognizer
from .hpo_exact_cr import HpoExactConceptRecognizer

HPO_JSON_URL = "http://purl.obolibrary.org/obo/hp/hp.json"


class HpoToolkitParser:
    """
    Class to retrieve and parse the HPO JSON file using the HPO-Toolkit
    """

    def __init__(self, hpo_json_file:str=None):
        if hpo_json_file is not None:
            if not os.path.isfile(hpo_json_file):
                raise FileNotFoundError(f"Could not find hp.json file at {hpo_json_file}")
            self._ontology = hpotk.load_minimal_ontology(hpo_json_file)
        else:
            self._ontology = hpotk.load_minimal_ontology(HPO_JSON_URL)

    def get_ontology(self):
        """
        :returns: a reference to the HPO
        :rtype: hpotk.MinimalOntology
        """
        return self._ontology

    def get_label_to_id_map(self):
        """
        :returns: a map from HPO term labels to HPO ids
        :rtype: Dict[str,str]
        """
        label_to_id_d = {}
        for t in self._ontology.terms:
            if t.is_obsolete:
                continue
            label_to_id_d[t.name] = t.identifier.value
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
