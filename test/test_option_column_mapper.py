import unittest
import os
from pyphetools import HpoParser, OptionColumnMapper, HpoConceptRecognizer

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')



class TestOptionMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        cls.severity_d = {'mild': 'Intellectual disability, mild',
             'moderate':'Intellectual disability, moderate',
             'severe': 'Intellectual disability, severe',
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
        

        
        