import re
import typing
import abc
from collections import defaultdict

from .hp_term import HpTerm
from .hpo_cr import HpoConceptRecognizer


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


class HpoBaseConceptRecognizer(HpoConceptRecognizer):

    def __init__(self, label_to_id, id_to_primary_label):
        if not isinstance(label_to_id, dict):
            raise ValueError("label_to_id_d argument must be dictionary")
        if not isinstance(id_to_primary_label, dict):
            raise ValueError("labels_to_primary_label_d argument must be dictionary")
        self._id_to_primary_label = id_to_primary_label
        self._label_to_id = label_to_id

    def parse_cell(self, cell_contents, custom_d=None) -> typing.List[HpTerm]:
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

    def _get_exact_match_in_custom_d(self, cell_text, custom_d) -> typing.List[HpTerm]:
        """This method is called by _parse_contents if cell_text was present in custom_d

        If the match does not result in at least one HpTerm match, it is an error and the custom_d probably has an incorrect string

        :param cell_text: The text of a table cell
        :type cell_text: str
        :param custom_d: key - text in original table value-corresponding HPO label
        :type custom_d: Dict[str, Union[str,List[str]]]
        :returns: list of HPO terms
        :rtype: List[HpTerm]
        """
        label = custom_d.get(cell_text)
        results = []
        if isinstance(label, list):
            for lab in label:
                hp_term = self.get_term_from_label(label=lab)
                if hp_term is None:
                    raise ValueError(f"Could not get HpTerm from {lab}")
                else:
                    results.append(hp_term)
        else:
            hp_term = self.get_term_from_label(label=label)
            if hp_term is None:
                raise ValueError(f"Could not get HpTerm from {label}")
            else:
                results.append(hp_term)
        return results

    def _find_text_within_custom_items(self, lc_chunk, custom_d) -> typing.List[HpTerm]:
        hits = []
        # Note that chunk has been stripped of whitespace and lower-cased already
        for original_text, hpo_label in custom_d.items():
            lc_original = original_text.lower()
            startpos = lc_chunk.find(lc_original)
            if startpos < 0:
                continue
            endpos = startpos + len(lc_original) - 1
            if isinstance(hpo_label, str):
                hp_term = self.get_term_from_label(hpo_label)
                hits.append(ConceptMatch(term=hp_term, start=startpos, end=endpos))
            elif isinstance(hpo_label, list):
                for h in hpo_label:
                    hp_term = self.get_term_from_label(h)
                    hits.append(ConceptMatch(term=hp_term, start=startpos, end=endpos))
        return hits

    @abc.abstractmethod
    def _find_hpo_term_in_lc_chunk(self, lc_chunk) -> typing.List[HpTerm]:
        pass

    def _parse_contents(self, cell_text, custom_d) -> typing.List[HpTerm]:
        """Parse the contents of a cell for HPO terms
        Args:
            cell_text (str): The text of a table cell
            custom_d (dict): key - text in original table value-corresponding HPO label
        """
        if cell_text in custom_d:
            return self._get_exact_match_in_custom_d(cell_text=cell_text, custom_d=custom_d)
        chunks = self._split_line_into_chunks(cell_text)
        results = []
        for chunk in chunks:
            lc_chunk = chunk.lower()
            hits_1 = self._find_text_within_custom_items(lc_chunk=lc_chunk, custom_d=custom_d)
            hits_2 = self._find_hpo_term_in_lc_chunk(lc_chunk=lc_chunk)
            hits_1.extend(hits_2)
            results.extend(self._get_non_overlapping_matches(hits=hits_1))
        return results

    def parse_cell_for_exact_matches(self, cell_text, custom_d) -> typing.List[HpTerm]:
        """
        Identify HPO Terms from the contents of a cell whose label exactly matches a string in the custom dictionary

        :param cell_contents: a cell of the original table
        :type cell_contents: str
        :param custom_d: a dictionary with keys for strings in the original table and their mappings to HPO labels
        :type custom_d: Dict[str,str]
        """
        if cell_text in custom_d:
            return self._get_exact_match_in_custom_d(cell_text=cell_text, custom_d=custom_d)
        chunks = self._split_line_into_chunks(cell_text)
        results = []
        for chunk in chunks:
            lc_chunk = chunk.lower()
            hits = self._find_text_within_custom_items(lc_chunk=lc_chunk, custom_d=custom_d)
            results.extend(self._get_non_overlapping_matches(hits=hits))
        return

    def _get_non_overlapping_matches(self, hits: typing.List[ConceptMatch]) -> typing.List[HpTerm]:
        """The prupose of this method is to choose a list of non-overlapping matches

        Sometimes, we get multiple matches that partially overlap. We will greedily take the longest matches and discard overlaps.

        :param hits: list of ConceptMatch objects that encode HpTerm matches and their positions
        :type hits: List[ConceptMatch]
        :returns: a list of non-overlapping HtTerm objects (matches)
        :rtype: List[HpTerm]
        """
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
        results = []
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

