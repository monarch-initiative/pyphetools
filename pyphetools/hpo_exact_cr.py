from .hpo_cr import HpoConceptRecognizer
from .hp_term import HpTerm

import re
import pandas as pd
from typing import List
from collections import defaultdict

class HpoExactConceptRecognizer(HpoConceptRecognizer):
    #self._label_to_id_d, self._id_to_primary_label
    def __init__(self, label_to_id, id_to_primary_label):
        super().__init__()
        if not isinstance(label_to_id, dict):
            raise ValueError("label_to_id_d argument must be dictionary")
        if not isinstance(id_to_primary_label, dict):
            raise ValueError("labels_to_primary_label_d argument must be dictionary")
        self._id_to_primary_label = id_to_primary_label
        self._label_to_id = label_to_id
        
        
    def parse_cell(self, cell_contents, custom_d=None)-> List[HpTerm]:
        """_summary_

        Args:
            cell_contents (_type_): description of patient phenotypes. Assumption is that if there are new lines, any given phenotype is on its own line
            custom_d (_type_, optional): User-provided dictionary with mappings to HPO terms. Defaults to None.

        Raises:
            ValueError: must be a string
        """
        if not isinstance(cell_contents, str):
            raise ValueError(f"Error: cell_contents argument must be string but was {type(cell_contents)}")
        chunks = cell_contents.split('\n')
        if len(chunks) > 1:
            results = []
            for chunk in chunks:
                res = self._parse_chunk(chunk_content=chunk, custom_d=custom_d)
                results.append(res)
        else:
            return self._parse_chunk(chunk_content=chunks[0], custom_d=custom_d)
            
            
    def _parse_chunk(self, chunk_content, custom_d) -> List[HpTerm]:
        """_summary_
        'private' function to parse one candidate hpo item
        Args:
            chunk_content (_type_): _description_
            custom_d (_type_): _description_
        """
        # remove whitespace, convert to lower case (as )
        content = chunk_content.strip().lower() 
        if content is None or len(content) == 0:
            return []
        print(f"parse chunk for {content}")
        if content in self._label_to_id:
            hpo_id = self._label_to_id.get(content)
            label = self._id_to_primary_label.get(hpo_id)
            return [HpTerm(id=hpo_id, label=label)]
        elif custom_d is not None and content in custom_d:
            hpo_id = self.custom_d.get(content)
            label = self._id_to_primary_label.get(hpo_id)
            return [HpTerm(id=hpo_id, label=label)]
        else:
            # if we get here, check if we can split the cell on some commonly used separators
            minichunks = re.split(',;|/', content) 
            results = []
            for mc  in minichunks:
                if mc in self._label_to_id:
                    hpo_id = self._label_to_id.get(mc)
                    label = self._id_to_primary_label.get(hpo_id)
                    results.append(HpTerm(id=hpo_id, label=label))
                elif custom_d is not None and mc in custom_d:
                    hpo_id = self.custom_d.get(mc)
                    label = self._id_to_primary_label.get(hpo_id)
                    results.append(HpTerm(id=hpo_id, label=label))
            return results