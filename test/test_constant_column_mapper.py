import unittest
from src.pyphetools.creation import ConstantColumnMapper



class TestConstantMapper(unittest.TestCase):
        
    def test_observed_constant(self):
        hp_id =  "HP:0031956"
        hp_label = "Elevated circulating aspartate aminotransferase concentration"
        mapper = ConstantColumnMapper(hpo_id=hp_id, hpo_label=hp_label)
        hp_term_list = mapper.map_cell("n/a")
        self.assertEqual(1, len(hp_term_list))
        result = hp_term_list[0]
        self.assertEqual(hp_id, result.id)
        self.assertEqual(hp_label, result.label)
        self.assertTrue(result.observed)
        
    def test_excluded_constant(self):
        hp_id =  "HP:0031956"
        hp_label = "Elevated circulating aspartate aminotransferase concentration"
        mapper = ConstantColumnMapper(hpo_id=hp_id, hpo_label=hp_label, excluded=True)
        hp_term_list = mapper.map_cell("n/a")
        self.assertEqual(1, len(hp_term_list))
        result = hp_term_list[0]
        self.assertEqual(hp_id, result.id)
        self.assertEqual(hp_label, result.label)
        self.assertFalse(result.observed)
        self.assertTrue(result.excluded)
