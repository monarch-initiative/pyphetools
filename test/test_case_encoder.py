import unittest
import os
import pandas as pd
from pyphetools import HpoParser, CaseEncoder
HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')
# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"

class TestCaseParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        hpparser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        hpo_cr = hpparser.get_hpo_concept_recognizer()
        cls._parser = CaseEncoder(concept_recognizer=hpo_cr, pmid="PMID:1")

    def test_chief_complait(self):
        """
        Expect to get
        HP:0000365 	Hearing impairment 	True 	True
1 	    HP:0001742 	Nasal congestion 	True 	True
2 	    HP:0025267 	Snoring
        """
        vignette = "A 17-mo-old boy presented with progressive nasal obstruction, snoring and hearing loss symptoms when referred to the hospital."
        results = self._parser.add_vignette(vignette=vignette)
        self.assertEqual(3, len(results))
        self.assertTrue(isinstance(results, pd.DataFrame))
        id = results.loc[(results['id'] == 'HP:0000365')]['id'].values[0]
        self.assertEqual("HP:0000365", id)

       