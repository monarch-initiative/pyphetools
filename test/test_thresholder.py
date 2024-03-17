import unittest
from pyphetools.creation import Thresholder



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

    def test_potassium(self):
        kThresholder = Thresholder.potassium_blood()
        hpterm = kThresholder.map_value(2)
        self.assertEqual("Hypokalemia", hpterm.label)
        self.assertEqual("HP:0002900", hpterm.id)

    def test_NTproBNP_blood(self):
        thresholder = Thresholder.NTproBNP_blood()
        hpterm = thresholder.map_value(200)
        self.assertEqual("Increased circulating NT-proBNP concentration", hpterm.label)
        self.assertEqual("HP:0031185", hpterm.id)

    def test_troponin_t_blood(self):
        thresholder = Thresholder.troponin_t_blood()
        hpterm = thresholder.map_value(20)
        self.assertEqual("Increased circulating troponin T concentration", hpterm.label)
        self.assertEqual("HP:0410174", hpterm.id)


    def test_nan_value(self):
        """A cell that has a nan value should map to not observed of the abnormal term
        """
        kThresholder = Thresholder.potassium_blood()
        hpterm = kThresholder.map_value("nan")
        self.assertEqual("Abnormal blood potassium concentration", hpterm.label)
        self.assertEqual("HP:0011042", hpterm.id)
        self.assertFalse(hpterm.measured)

    def test_nan_float_value(self):
        """A cell that has a nan value should map to not observed of the abnormal term
        """
        kThresholder = Thresholder.potassium_blood()
        hpterm = kThresholder.map_value(float('nan'))
        self.assertEqual("Abnormal blood potassium concentration", hpterm.label)
        self.assertEqual("HP:0011042", hpterm.id)
        self.assertFalse(hpterm.measured)