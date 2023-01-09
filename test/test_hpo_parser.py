import unittest
import os
from pyphetools.creation import HpoParser

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')

class TestHpoParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        
    def test_not_none(self):
        self.assertIsNotNone(self.hpo_cr)
