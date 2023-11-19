import unittest

from src.pyphetools.creation import HpTerm


class TestHpTerm(unittest.TestCase):

    def test_excluded(self):
        hpo_term = HpTerm(hpo_id="HP:0001250", label="test label")
        self.assertEqual("HP:0001250", hpo_term.id)
        self.assertEqual("test label", hpo_term.label)
        self.assertTrue(hpo_term.observed)
        self.assertTrue(hpo_term.measured)
        hpo_term.excluded()
        self.assertFalse(hpo_term.observed)
        
        
    def test_create_phenotypic_feature(self):
        """test creation of GA4GH PhenotypicFeature object with onset and resolution
        """
        hpo_term = HpTerm(hpo_id="HP:0001250", label="test label", onset="P2M", resolution="P6M")
        self.assertEqual("HP:0001250", hpo_term.id)
        self.assertEqual("test label", hpo_term.label)
        self.assertEqual("P2M", hpo_term.onset)
        self.assertEqual("P6M", hpo_term.resolution)
        self.assertTrue(hpo_term.observed)
        self.assertTrue(hpo_term.measured)
        pfeat = hpo_term.to_phenotypic_feature()
        self.assertIsNotNone(pfeat)
        pfterm = pfeat.type
        self.assertEqual("HP:0001250", pfterm.id)
        self.assertEqual("test label", pfterm.label)
        self.assertEqual("P2M", pfeat.onset.age.iso8601duration)
        self.assertEqual("P6M", pfeat.resolution.age.iso8601duration)
        self.assertFalse(pfeat.excluded)
        
