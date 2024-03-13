import unittest
from pyphetools.creation import ThresholdedColumnMapper, Thresholder
from pyphetools.creation import HpTerm

class TestThresholdedColumnMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        high = HpTerm(hpo_id="HP:0003155",label="Elevated circulating alkaline phosphatase concentration")
        low = HpTerm(hpo_id="HP:0003282",label="Low alkaline phosphatase")
        abn =  HpTerm(hpo_id="HP:0004379",label="Abnormality of alkaline phosphatase level")
        thresholder = Thresholder(hpo_term_high=high,
                                hpo_term_abn=abn,
                                hpo_term_low=low,
                                threshold_low=30,
                                threshold_high=120,
                                unit="U/L")
        #alkaline phosphatase concentration
        cls.mapper = ThresholdedColumnMapper(column_name="placeholder",
                                            thresholder=thresholder)

    def test_threshold_of_3(self):
        res = self.mapper.map_cell(3)
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0003282", result.id)
        self.assertEqual("Low alkaline phosphatase", result.label)
        self.assertTrue(result.observed)

    def test_threshold_of_400(self):
        res = self.mapper.map_cell(400)
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0003155", result.id)
        self.assertEqual("Elevated circulating alkaline phosphatase concentration", result.label)
        self.assertTrue(result.observed)

    def test_threshold_of_61(self):
        # normal result
        res = self.mapper.map_cell(61.1)
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0004379", result.id)
        self.assertEqual("Abnormality of alkaline phosphatase level", result.label)
        self.assertFalse(result.observed)

    def test_threshold_with_na(self):
        """_summary_
        Return cannot be measured if the threshold cannot be read
        """
        res = self.mapper.map_cell("NA")
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0004379", result.id)
        self.assertEqual("Abnormality of alkaline phosphatase level", result.label)
        self.assertFalse(result.measured)
