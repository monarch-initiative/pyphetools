import unittest
from src.pyphetools.creation import AgeIsoFormater



class TestAgeIsoFormater(unittest.TestCase):

    def test_basic1(self):
        iso_age = AgeIsoFormater.to_string(y=2, m=3, d=5)
        self.assertEqual("P2Y3M5D", iso_age)

    def test_basic2(self):
        """
        test that 13 months are normalized to 1 year 1 month
        """
        iso_age = AgeIsoFormater.to_string(y=42, m=13, d=5)
        self.assertEqual("P43Y1M5D", iso_age)

    def test_5m(self):
        iso_age = AgeIsoFormater.from_numerical_month(5)
        self.assertEqual("P5M", iso_age)

    def test_15d(self):
        iso_age = AgeIsoFormater.from_numerical_month(0.5)
        self.assertEqual("P15D", iso_age)

    def test_24d(self):
        iso_age = AgeIsoFormater.from_numerical_month(0.8)
        self.assertEqual("P24D", iso_age)

    def test_12m(self):
        iso_age = AgeIsoFormater.from_numerical_month(12)
        self.assertEqual("P1Y", iso_age)

    def test_16m(self):
        iso_age = AgeIsoFormater.from_numerical_month(16)
        self.assertEqual("P1Y4M", iso_age)

    def test_na(self):
        """
        Test we return NOT_PROVIDED (from the Contants class) if we cannot parse the cell contents
        """
        iso_age = AgeIsoFormater.from_numerical_month("n.a.")
        self.assertEqual("NOT_PROVIDED", iso_age)

    def test_none(self):
        """
        Test we return NOT_PROVIDED (from the Contants class) if we cannot parse the cell contents
        """
        iso_age = AgeIsoFormater.from_numerical_month(None)
        self.assertEqual("NOT_PROVIDED", iso_age)

    def test_nan(self):
        """
        Test we return NOT_PROVIDED (from the Contants class) if we cannot parse the cell contents
        """
        iso_age = AgeIsoFormater.from_numerical_month(float("nan"))
        self.assertEqual("NOT_PROVIDED", iso_age)

    def test_newborn(self):
        iso_age = AgeIsoFormater.from_numerical_month(0)
        self.assertEqual("P0D", iso_age)



