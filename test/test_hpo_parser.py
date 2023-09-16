import unittest
import os
from src.pyphetools.creation import HpoParser

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')

class TestHpoParser(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        
    def test_not_none(self):
        self.assertIsNotNone(self.hpo_cr)

    def test_deprecated_nodes_not_parsed(self):
        """Test that the parser did not ingest a deprecated node"""
        # HP_0000284 is for the obsoleted term obsolete Abnormality of the ocular region
        self.assertFalse(self.hpo_cr.contains_term("HP0000284"))
        # HP:0000319 for for the valid term Smooth philtrum
        self.assertTrue(self.hpo_cr.contains_term("HP:0000319"))
