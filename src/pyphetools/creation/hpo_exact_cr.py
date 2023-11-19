import hpotk

from .hpo_cr import HpoConceptRecognizer
from .hp_term import HpTerm
from .column_mapper import ColumnMapper
from .simple_column_mapper import SimpleColumnMapper

import re
from typing import List
from collections import defaultdict


class ConceptMatch:
    def __init__(self, term, start: int, end: int) -> None:
        self._hp_term = term
        self._start = start
        self._end = end

    def length(self):
        return 1 + (self._end - self._start)

    @property
    def label(self):
        return self._hp_term.label

    @property
    def tid(self):
        return self._hp_term.id

    @property
    def term(self):
        return self._hp_term

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def overlaps(self, other):
        if self.end >= other.start >= self.start:
            return True
        elif self.end >= other.end >= self.start:
            return True
        else:
            return False


class HpoExactConceptRecognizer(HpoConceptRecognizer):
    # self._label_to_id_d, self._id_to_primary_label
    def __init__(self, label_to_id, id_to_primary_label, ontology:hpotk.Ontology=None):
        super().__init__()
        if not isinstance(label_to_id, dict):
            raise ValueError("label_to_id_d argument must be dictionary")
        if not isinstance(id_to_primary_label, dict):
            raise ValueError("labels_to_primary_label_d argument must be dictionary")
        self._id_to_primary_label = id_to_primary_label
        self._label_to_id = label_to_id
        self._ontology = ontology

    def parse_cell(self, cell_contents, custom_d=None) -> List[HpTerm]:
        """parse the contents of one table cell

        Args:
            cell_contents (str): description of patient phenotypes. Assumption is that if there are new lines, any given phenotype is on its own line
            custom_d (dict, optional): User-provided dictionary with mappings to HPO terms. Defaults to None.
        """
        if not isinstance(cell_contents, str):
            print(
                f"Error: cell_contents argument ({cell_contents}) must be string but was {type(cell_contents)} -- coerced to string")
            cell_contents = str(cell_contents)

        # lines = self._split_into_lines(cell_contents)
        cell_text = cell_contents.replace("\n", " ")
        if custom_d is None:
            # initialize to empty dictionary if this argument is not passed
            # to avoid needed to check for None in other functions
            custom_d = defaultdict()
        return self._parse_contents(cell_text=cell_text, custom_d=custom_d)

    def _parse_contents(self, cell_text, custom_d) -> List[HpTerm]:
        """Parse the contents of a cell for HPO terms
        Args:
            cell_text (str): THe text of a table cell
            custom_d (dict): key - text in original table value-corresponding HPO label
        """
        if cell_text in custom_d:
            label = custom_d.get(cell_text)
            results = []
            if isinstance(label, list):
                for lab in label:
                    hp_term = self.get_term_from_label(label=lab)
                    if hp_term is not None:
                        results.append(hp_term)
            else:
                hp_term = self.get_term_from_label(label=label)
                results.append(hp_term)
            return results
        chunks = self._split_line_into_chunks(cell_text)
        results = []
        for chunk in chunks:
            lc_chunk = chunk.lower()
            hits = []
            # Note that chunk has been stripped of whitespace and lower-cased already
            for original_text, hpo_label in custom_d.items():
                lc_original = original_text.lower()
                startpos = lc_chunk.find(lc_original)
                if startpos < 0:
                    continue
                endpos = startpos + len(lc_original) - 1
                hp_term = self.get_term_from_label(hpo_label)
                hits.append(ConceptMatch(term=hp_term, start=startpos, end=endpos))
            for lower_case_hp_label, hpo_tid in self._label_to_id.items():
                key = lower_case_hp_label.lower()
                startpos = chunk.find(key)
                endpos = startpos + len(key) - 1
                if startpos < 0:
                    continue
                # If we get here, we demand that the match is a complete word
                # This is because otherwise we get some spurious matches such as Pica HP:0011856 matching to typical
                # Create a regex to enforce the match is at word boundary
                BOUNDARY_REGEX = re.compile(r'\b%s\b' % key, re.I)
                if BOUNDARY_REGEX.search(chunk):
                    hp_term = self.get_term_from_id(hpo_id=hpo_tid)  # Get properly capitalized label
                    hits.append(ConceptMatch(term=hp_term, start=startpos, end=endpos))
            # sort hits according to length
            sorted_hits = sorted(hits, key=ConceptMatch.length, reverse=True)
            # Choose longest hits first and skip hits that overlap with previously chosen hits
            chosen_hits = set()
            for hit in sorted_hits:
                keeper = True
                for ch in chosen_hits:
                    if ch.overlaps(hit):
                        keeper = False
                        break
                if keeper:
                    chosen_hits.add(hit)
            for ch in chosen_hits:
                results.append(ch.term)
        return results

    def _split_line_into_chunks(self, line):
        """Split a line into chunks and remove white space from beginning and end of each chunk

        Args:
            line (str): one line of a potentially multi-line Table cell.
        """
        delimiters = ',;|/'
        regex_pattern = '|'.join(map(re.escape, delimiters))
        chunks = re.split(regex_pattern, line)
        return [chunk.strip().lower() for chunk in chunks]

    def get_term_from_id(self, hpo_id) -> HpTerm:
        if not hpo_id.startswith("HP:"):
            raise ValueError(f"Malformed HP id '{hpo_id}' - must start with HP:")
        if hpo_id not in self._id_to_primary_label:
            raise ValueError(f"Could not find id {hpo_id} in dictionary")
        label = self._id_to_primary_label.get(hpo_id)
        return HpTerm(hpo_id=hpo_id, label=label)

    def get_term_from_label(self, label) -> HpTerm:
        label_lc = label.lower()  # the dictionary was constructed in lower case!
        if label_lc not in self._label_to_id:
            raise ValueError(f"Could not find HPO id for {label}")
        hpo_id = self._label_to_id.get(label_lc)
        return HpTerm(hpo_id=hpo_id, label=label)

    def contains_term(self, hpo_id) -> bool:
        return hpo_id in self._id_to_primary_label

    def contains_term_label(self, hpo_label) -> bool:
        """return True iff the argument is the primary label of an HPO term
        """
        return hpo_label.lower() in self._label_to_id

    def initialize_simple_column_maps(self, column_name_to_hpo_label_map, observed, excluded, non_measured=None):
        if observed is None or excluded is None:
            raise ValueError("Symbols for observed (e.g., +, Y, yes) and excluded (e.g., -, N, no) required")
        if not isinstance(column_name_to_hpo_label_map, dict):
            raise ValueError("column_name_to_hpo_label_map must be a dict with column to HPO label mappings")
        simple_mapper_d = defaultdict(ColumnMapper)
        for column_name, hpo_label_and_id in column_name_to_hpo_label_map.items():
            if not isinstance(hpo_label_and_id, list):
                raise ValueError(f"Expected {hpo_label_and_id} to be a two-item list with HPO label and id")
            hpo_label = hpo_label_and_id[0]
            expected_id = hpo_label_and_id[1]
            hp_term = self.get_term_from_label(hpo_label)
            if hp_term.id != expected_id:
                raise ValueError(f"Got {hp_term.id} but was expecting {expected_id} for {hpo_label}")
            mpr = SimpleColumnMapper(hpo_id=hp_term.id, hpo_label=hp_term.label, observed=observed, excluded=excluded)
            simple_mapper_d[column_name] = mpr
        return simple_mapper_d

    def get_hpo_ontology(self):
        """
        :returns: a reference to the HPO-toolkit Ontology object for the HPO
        :rtype: hpotk.MinimalOntology
        """
        return self._ontology
