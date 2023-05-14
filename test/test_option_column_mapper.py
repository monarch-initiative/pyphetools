import unittest
import os
from pyphetools.creation import HpoParser, OptionColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestOptionMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        cls.severity_d = {'mild': ['Intellectual disability, mild', 'HP:0001256'],
                          'moderate': ['Intellectual disability, moderate','HP:0002342'],
                          'severe': ['Intellectual disability, severe', 'HP:0010864']
                          }

    def test_hpo_cr_mild(self):
        """We should retrieve Intellectual disability, mild (HP:0001256)"""
        optionMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=self.severity_d)
        results = optionMapper.map_cell("mild")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0001256", result.id)
        self.assertEqual("Intellectual disability, mild", result.label)

    def test_hpo_cr_moderate(self):
        """We should retrieve Intellectual disability, moderate (HP:0002342)"""
        optionMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=self.severity_d)
        results = optionMapper.map_cell("moderate")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0002342", result.id)
        self.assertEqual("Intellectual disability, moderate", result.label)

    def test_hpo_cr_severe(self):
        """We should retrieve Intellectual disability, severe (HP:0010864) """
        optionMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=self.severity_d)
        results = optionMapper.map_cell("severe")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0010864", result.id)
        self.assertEqual("Intellectual disability, severe", result.label)

    def test_with_acronyms(self):
        other_d = {
            "HP": ["High palate", "HP:0000218"],
            "D": ["Dolichocephaly", "HP:0000268"],
            "En": ["Deeply set eye", "HP:0000490"],  # i.e., Enophthalmus
            "DE": ["Dural ectasia", "HP:0100775"],
            "St": ["Striae distensae", "HP:0001065"]
        }
        otherMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=other_d)
        res1 = otherMapper.map_cell("HP")
        self.assertIsNotNone(res1)
        self.assertEqual(1, len(res1))
        hpterm = res1[0]
        self.assertEqual("High palate", hpterm.label)
        self.assertEqual("HP:0000218", hpterm.id)
        res2 = otherMapper.map_cell("HP,D")
        self.assertIsNotNone(res2)
        self.assertEqual(2, len(res2))
        hpterm = res2[0]
        self.assertEqual("High palate", hpterm.label)
        self.assertEqual("HP:0000218", hpterm.id)
        hpterm = res2[1]
        self.assertEqual("Dolichocephaly", hpterm.label)
        self.assertEqual("HP:0000268", hpterm.id)

