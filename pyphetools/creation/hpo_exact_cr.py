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
            print(f"Error: cell_contents argument ({cell_contents}) must be string but was {type(cell_contents)} -- coerced to string")
            cell_contents = str(cell_contents)   
            
        lines = self._split_into_lines(cell_contents)
        if custom_d is None:
            # initialize to empty dictionary if this argument is not passed 
            # to avoid needed to check for None in other functions
            custom_d = defaultdict()
        if len(lines) > 1:
            results = []
            for line in lines:
                res = self._parse_line(line=line, custom_d=custom_d)
                results.append(res)
        else:
            # just one line
            return self._parse_line(line=lines[0], custom_d=custom_d)
        
    def _split_into_lines(self, cell_contents):
        """_summary_
        Split a cell into lines and remove white space from beginning and end of each line and transform to lower case
        """
        return cell_contents.split('\n')
    
    def _split_line_into_chunks(self, line):
        """_summary_
        Split a line into chunks and remove white space from beginning and end of each chunk
        """
        delimiters = ',;|/'
        regex_pattern = '|'.join(map(re.escape, delimiters))
        chunks = re.split(regex_pattern, line) 
        return [chunk.strip().lower() for chunk in chunks]
    
    def _parse_chunk(self, chunk, custom_d) -> List[HpTerm]:
        if chunk in custom_d:
            label = custom_d.get(chunk)
            hpo_id = self._label_to_id[label.lower()]
            return [HpTerm(id=hpo_id, label=label)]
        else:
            results = []
            # If we get here, we do two things
            # We may have a long text that includes both custom strings and HPO terms/synonyms
            # strategy is to first extract the custom terms and then check the remaining text
            # for HPO terms
            remaining_text = chunk.lower()
            for k, v in custom_d.items():
                key = k.lower()
                # We now try to find a custom item in the potentially longer chunk string
                if key in remaining_text:
                    hpo_label = v
                    hpo_label_lc = hpo_label.lower()    
                    hpo_id = self._label_to_id.get(hpo_label_lc)
                    if hpo_id is None:
                        print(f"Unable to retrieve HPO Id for custom mapping {chunk} -> {hpo_label}")
                        return []
                    results.append(HpTerm(id=hpo_id, label=hpo_label))
                    remaining_text = remaining_text.replace(key, " ")
            # When we get here, we look for HPO terms in the remaining text
            if len(remaining_text) > 5:
                for k, v in custom_d.items():
                    key = k.lower()
                    if key in remaining_text:
                        hpo_id = v
                        hpo_label = self._id_to_primary_label.get(hpo_id)
                        results.append(HpTerm(id=hpo_id, label=hpo_label))
                        remaining_text = remaining_text.replace(key, " ")
                        #print(f"hpo {hpo_label} key {key} remaining {remaining_text}")
            return results
            
    def _parse_line(self, line, custom_d) -> List[HpTerm]:
        """_summary_
        'private' function to parse an entire line or chunk
        The reason we parse lines first is that we are more likely to get complete HPO terms this way
        """
        # remove whitespace, convert to lower case (as )
        content = line.strip().lower() 
        if content is None or len(content) == 0:
            return []
        results = self._parse_chunk(chunk=content, custom_d=custom_d)
        if len(results) > 0:
            return results
        else:
            chunks = self._split_line_into_chunks(content)
            results = []
            for chunk in chunks:
                # Note that chunk has been stripped of whitespace and lower-cased already
                res = self._parse_chunk(chunk=chunk, custom_d=custom_d)
                results.extend(res)
            return results

    def get_term_from_id(self, id) -> HpTerm:
        if not id.startswith("HP:"):
            raise ValueError(f"Malformed HP id '{id}' - must start with HP:")
        if not id in self._id_to_primary_label:
            raise ValueError(f"Could not find id {id} in dictionary")
        label = self._id_to_primary_label.get(id)
        return HpTerm(id=id, label=label)