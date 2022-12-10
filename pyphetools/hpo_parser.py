import json
from collections import defaultdict
from .hpo_cr import HpoConceptRecognizer
from .hpo_exact_cr import HpoExactConceptRecognizer



class HpoParser:
    """
    Extract maps of labels and ids from the hp.json file.
    Note that we do not need to have the ontological structure of the HPO for this
    application and so only nodes and version are extracted.
    """
    def __init__(self, hpo_json_file):
        with open(hpo_json_file) as f:
            data = json.load(f)  
            graphs = data.get('graphs')
        if len(graphs) != 1:
            raise ValueError(f"Expected to get one graph but got {len(graphs)}")
        hpo = graphs[0]
        id = hpo.get("id")
        if id != "http://purl.obolibrary.org/obo/hp.json":
            raise ValueError(f"Expected to get hp.json but got {id}")  
        nodes = hpo.get("nodes")    
        id_to_primary_label = defaultdict()
        label_to_id = defaultdict()
        for n in nodes:
            if 'id' in n and 'HP_' in n.get('id'):
                hpo_id, label, all_labels = self._extract_node_data(n)
                id_to_primary_label[hpo_id] =  label
                for lab in all_labels:
                    label_to_id[lab.lower()] = hpo_id
        self._id_to_primary_label = id_to_primary_label
        self._label_to_id = label_to_id
        meta = hpo.get('meta')
        long_version = meta.get('version')
        if 'http://purl.obolibrary.org/obo/hp/releases/' in long_version:
            version = long_version[43:].split('/')[0]
        else:
            version = long_version
        self._long_version = long_version
        self._version = version

    def _extract_node_data(self, json_node):
        if not isinstance(json_node, dict):
            raise ValueError("HpoNode obhject must be constructed from JSON-derived dictionary")
        if not 'id' in json_node.keys():
            raise ValueError("HpoNode object must have id attribute")
        id = json_node.get('id')
        if not 'lbl' in json_node.keys():
            raise ValueError(f"HpoNode object must have lbl attribute but {id} did not")
        if not 'http://purl.obolibrary.org/obo/HP' in id:
            raise ValueError(f"HpoNode id must begin with 'http://purl.obolibrary.org/obo/' but we got {id}")
        hpo_id = id[31:].replace("_", ":")
        label = json_node.get("lbl","NA")
        all_labels = [label]
        if 'synonyms' in json_node:
            syns = json_node.get('synonyms')
            for syn in syns:
                synonym = syn.get('val')
                all_labels.append(synonym)
        return hpo_id, label, all_labels 

    def get_version(self):
        return self._version
    
    def get_hpo_concept_recognizer(self) -> HpoConceptRecognizer:
        return HpoExactConceptRecognizer(label_to_id=self._label_to_id, id_to_primary_label=self._id_to_primary_label)