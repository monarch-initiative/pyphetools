import json
from collections import defaultdict
from .hpo_cr import HpoConceptRecognizer
from .hpo_exact_cr import HpoExactConceptRecognizer
import urllib.request 
import os


HPO_JSON_URL = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.json"


def extract_curie(url):
    if not url.startswith('http://purl.obolibrary.org/obo/HP'):
        return None
    return url[31:].replace("_", ":")

class Edge:
    """_summary_
    This class represents an is-a link in the HPO graph.
    Note that instances of this class are not intended for use outside of parsing, where we use them to 
    restrict the terms that are return to descendants of Phenotypic abnormality (HP:0000118).
    """
    def __init__(self, e) -> None:
        self._subject = extract_curie(e.get('sub'))
        self._object = extract_curie(e.get('obj'))
        
    def is_valid(self):
        return self._subject is not None and self._object is not None
    
    @property
    def subject(self):
        return self._subject
    
    @property
    def object(self):
        return self._object

def is_phenotype(hpo_id, subject_to_edge_d):
    """_summary_
    return True if hpo_id is a descendant of HP:0000118, Phenotypic abnormality, otherwise return False
    Args:
        hpo_id (str): a candidate HPO term
        subject_to_edge_d (dict): subject: HPO CURIE; object: list of Edges with this CURIE as subject

    Returns:
        bool: return True if hpo_id is a descendant of HP:0000118, otherwise False
    """
    stack = [hpo_id]
    while len(stack) > 0:
        id = stack.pop()
        parent_edges = subject_to_edge_d.get(id, [])
        for p in parent_edges:
            if p.object == "HP:0000118":
                return True
            stack.append(p.object)
    return False
   
    
def extract_phenotype_descendant_ids(nodes, edges):
    """_summary_
    Create a simple graph structure and extract those HPO terms that are descendants
    of the Phenotypic abnormality
    Returns:
        Set: set of valid HPO terms describing only phenotypic abnormalities
    """
    # subject: HPO CURIE; object: list of Edges with this CURIE as subject
    subject_to_edge_d = defaultdict(list)
    for e in edges:
        edge = Edge(e)
        if edge.is_valid():
            subject_to_edge_d[edge.subject].append(edge)
    valid_nodes = set() 
    for n in nodes:
        node_id = extract_curie(n.get('id'))
        if node_id is not None and node_id.startswith("HP:"):
            if is_phenotype(node_id, subject_to_edge_d): 
                valid_nodes.add(node_id)
    return valid_nodes


class HpoParser:
    """
    Extract maps of labels and ids from the hp.json file.
    Note that we do not need to have the ontological structure of the HPO for this
    application and so only nodes and version are extracted.
    """
    def __init__(self, hpo_json_file=None):
        if hpo_json_file is None:
            hpo_json_file = self._download_to_disk_if_necessary()
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
        edges = hpo.get("edges")
        valid_node_curies = extract_phenotype_descendant_ids(nodes=nodes, edges=edges)  
        id_to_primary_label = defaultdict()
        label_to_id = defaultdict()
        for n in nodes:
            if 'id' in n and 'HP_' in n.get('id'):
                hpo_id, label, all_labels = self._extract_node_data(n)
                if not hpo_id in valid_node_curies:
                    continue # This restricts us to descendants of Phenotypic abnormality
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
        all_labels = set()
        all_labels.add(label)
        # synonyms are nest
        metadata = json_node.get('meta')
        if metadata is not None:
            synonyms = metadata.get('synonyms', None)
            if synonyms is not None:
                for syn in synonyms:
                    synonym = syn.get('val')
                    if len(synonym) < 5:
                        continue
                    all_labels.add(synonym)
        return hpo_id, label, list(all_labels)
    
    def _download_to_disk_if_necessary(self):
        local_dir = "hpo_data"
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        hpo_json_file = os.path.join(local_dir, "hp.json")
        if not os.path.isfile(hpo_json_file):
            urllib.request.urlretrieve(HPO_JSON_URL, hpo_json_file)
        return hpo_json_file
        

    def get_version(self):
        return self._version
    
    def get_hpo_concept_recognizer(self) -> HpoConceptRecognizer:
        return HpoExactConceptRecognizer(label_to_id=self._label_to_id, id_to_primary_label=self._id_to_primary_label)