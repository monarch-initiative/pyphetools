import unittest
from pyphetools.creation import HpTerm


class TestHpTerm(unittest.TestCase):

    def test_excluded(self):
        hpo_term = HpTerm(hpo_id="HP:0001250", label="test label")
        self.assertEqual("HP:0001250", hpo_term.id)
        self.assertEqual("test label", hpo_term.label)
        self.assertTrue(hpo_term.observed)
        self.assertTrue(hpo_term.measured)
        hpo_term.excluded()
        self.assertFalse(hpo_term.observed)
