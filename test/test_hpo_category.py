import unittest
import os
from src.pyphetools.visualization import HpoCategorySet

from hpotk.ontology.load.obographs import load_ontology

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestHpoCategorySet(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._hpo_ontology = load_ontology(HP_JSON_FILENAME)
        cls._category_set = HpoCategorySet(ontology=cls._hpo_ontology)
       
    def check_ataxia(self):
        """
        Ataxia HP:0001251
        """
        cat = self._category_set.get_category("HP:0001251")
        expected = "nervous_system"
        self.assertEqual(expected, cat)

    def check_category_level_term(self):
        """
        Abnormality of the nervous system HP:0000707
        """
        cat = self._category_set.get_category("HP:0000707")
        expected = "nervous_system"
        self.assertEqual(expected, cat)

