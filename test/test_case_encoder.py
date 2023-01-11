import unittest
import os
import pandas as pd
from pyphetools.creation import HpoParser, CaseEncoder
HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')
# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"

class TestCaseParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        hpparser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls._hpo_cr = hpparser.get_hpo_concept_recognizer()
        cls._parser = CaseEncoder(concept_recognizer=cls._hpo_cr, pmid="PMID:1")

    def test_chief_complaint(self):
        """
        Expect to get
        HP:0000365 	Hearing impairment 	True 	True
        HP:0001742 	Nasal congestion 	True 	True
        HP:0025267 	Snoring
        """
        vignette = "A 17-mo-old boy presented with progressive nasal obstruction, snoring and hearing loss symptoms when referred to the hospital."
        results = self._parser.add_vignette(vignette=vignette)
        self.assertEqual(3, len(results))
        self.assertTrue(isinstance(results, pd.DataFrame))
        id = results.loc[(results['id'] == 'HP:0000365')]['id'].values[0]
        self.assertEqual("HP:0000365", id)

    def test_excluded(self):
        """
        Currently, our text mining does not attempt to detect negation, but users can enter a set of term labels that are excluded
        In this case, He had no nasal obstruction should lead to excluded/Nasal congestion
        """
        vignette = "He had no nasal obstruction and he stated that his smell sensation was intact."
        excluded = set()
        excluded.add("Nasal congestion")
        results = self._parser.add_vignette(vignette=vignette, excluded_terms=excluded)
        self.assertEqual(1, len(results))
        id = results.loc[(results['id'] == 'HP:0001742')]['id'].values[0]
        self.assertEqual("HP:0001742", id)
        label = results.loc[(results['id'] == 'HP:0001742')]['label'].values[0]
        self.assertEqual("Nasal congestion", label)
        observed = results.loc[(results['id'] == 'HP:0001742')]['observed'].values[0]
        self.assertFalse(observed)
        measured = results.loc[(results['id'] == 'HP:0001742')]['measured'].values[0]
        self.assertTrue(measured)

    def test_excluded2(self):
        """
        The goal if this test is to enzure that 'Seizure' is annotated as 'excluded'
        """
        vignette = "The patient is not on seizure medication at this time."
        excluded = set()
        excluded.add("Seizure")
        encoder = CaseEncoder(concept_recognizer=self._hpo_cr, pmid="PMID:1")
        df = encoder.add_vignette(vignette=vignette, excluded_terms=excluded)
        self.assertEqual(1, len(df))
        
        self.assertEqual("HP:0001250", df.iloc[0]['id'])
        self.assertEqual("Seizure",df.iloc[0]['label'])
        self.assertFalse(df.iloc[0]['observed'])
        self.assertTrue(df.iloc[0]['measured'])

