import unittest
from src.pyphetools.creation import Thresholder



class TestThresholder(unittest.TestCase):

    def test_alk_phos(self):
        # 30-120
        apThresholder = Thresholder.alkaline_phophatase_blood()
        hpterm = apThresholder.map_value(12)
        # Low alkaline phosphatase (HP:0003282)
        self.assertEqual("Low alkaline phosphatase", hpterm.label)
        self.assertEqual("HP:0003282", hpterm.id)
        self.assertTrue(hpterm.observed)
        # Elevated circulating alkaline phosphatase concentration (HP:0003155)
        hpterm = apThresholder.map_value(500)
        self.assertEqual("Elevated circulating alkaline phosphatase concentration", hpterm.label)
        self.assertEqual("HP:0003155", hpterm.id)
        self.assertTrue(hpterm.observed)
        # Abnormality of alkaline phosphatase level (HP:0004379)
        hpterm = apThresholder.map_value(60) # normal value
        self.assertEqual("Abnormality of alkaline phosphatase level", hpterm.label)
        self.assertEqual("HP:0004379", hpterm.id)
        self.assertFalse(hpterm.observed)
        print(hpterm)
