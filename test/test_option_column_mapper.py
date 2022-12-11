import unittest
import os
from pyphetools import HpoParser, ColumnMapper, HpoConceptRecognizer

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')

class TestOptionMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        