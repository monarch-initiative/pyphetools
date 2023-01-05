import unittest
import os
from pyphetools import AgeColumnMapper
from pyphetools import HpoParser, CaseParser

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')
# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"

class TestCaseParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        hpparser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        hpo_cr = hpparser.get_hpo_concept_recognizer()
        cls._parser = CaseParser(concept_recognizer=hpo_cr, pmid="PMID:1")

    def test_chief_complait(self):
        vignette = "A 17-mo-old boy presented with progressive nasal obstruction, snoring and hearing loss symptoms when referred to the hospital."
        results = self._parser .add_vignette(vignette=vignette)
        self.assertEqual(1, len(results))