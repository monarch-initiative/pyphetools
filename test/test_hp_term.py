
import unittest
from pyphetools.creation import HpTerm

class TestHpTerm(unittest.TestCase):

    def test_excluded(self):
        hpterm = HpTerm(id="HP:0001250", label="test label")
        self.assertEqual("HP:0001250", hpterm.id)
        self.assertEqual("test label", hpterm.label)
        self.assertTrue(hpterm.observed)
        self.assertTrue(hpterm.measured)
        hpterm.excluded()
        self.assertFalse(hpterm.observed)







