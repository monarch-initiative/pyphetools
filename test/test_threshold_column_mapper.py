import unittest
from src.pyphetools.creation import ThresholdedColumnMapper


class TestThresholdedColumnMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mapper = ThresholdedColumnMapper(hpo_id="HP:0032988",
                                             hpo_label="Persistent head lag",
                                             threshold=4,
                                             call_if_above=True)

    def test_threshold_of_3(self):
        res = self.mapper.map_cell(3)
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0032988", result.id)
        self.assertEqual("Persistent head lag", result.label)
        self.assertFalse(result.observed)

    def test_threshold_of_4(self):
        res = self.mapper.map_cell(4)
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0032988", result.id)
        self.assertEqual("Persistent head lag", result.label)
        self.assertFalse(result.observed)

    def test_threshold_of_4_point_1(self):
        res = self.mapper.map_cell(4.1)
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0032988", result.id)
        self.assertEqual("Persistent head lag", result.label)
        self.assertTrue(result.observed)

    def test_threshold_with_na(self):
        """_summary_
        Return cannot be measured if the threshold cannot be read
        """
        res = self.mapper.map_cell("NA")
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        result = res[0]
        self.assertEqual("HP:0032988", result.id)
        self.assertEqual("Persistent head lag", result.label)
        self.assertFalse(result.measured)
