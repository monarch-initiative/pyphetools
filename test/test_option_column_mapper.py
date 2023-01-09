import unittest
import os
from pyphetools.creation import HpoParser, OptionColumnMapper, HpoConceptRecognizer

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
        
    def test_multiple_items_in_cell_1(self):
        seizure_d = {'Absence': 'Typical absence seizure',
                 'Infantile spasms': 'Infantile spasms',
               'GTC':'Bilateral tonic-clonic seizure',
                'ESES': 'Status epilepticus'}
        seizureMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=seizure_d)
        results = seizureMapper.map_cell("Absence")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0011147", result.id)
        self.assertEqual("Typical absence seizure", result.label) 
        self.assertTrue(result.observed)
        self.assertTrue(result.measured)
    
    def test_multiple_items_in_cell_2(self):
        seizure_d = {'Absence': 'Typical absence seizure',
                 'Infantile spasms': 'Infantile spasms',
               'GTC':'Bilateral tonic-clonic seizure',
                'ESES': 'Status epilepticus'}
        seizureMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=seizure_d)
        results = seizureMapper.map_cell("Absence and GTC")
        self.assertEqual(2, len(results))
        results = sorted(results, key=lambda x: x.id, reverse=True)
        result = results[0]
        self.assertEqual("HP:0011147", result.id)
        self.assertEqual("Typical absence seizure", result.label) 
        self.assertTrue(result.observed)
        self.assertTrue(result.measured)
        result = results[1]
        self.assertEqual("HP:0002069", result.id)
        self.assertEqual("Bilateral tonic-clonic seizure", result.label) 
        self.assertTrue(result.observed)
        self.assertTrue(result.measured)
        
    def test_multiple_items_in_cell_3(self):
        morph_d = {
            'bulbous nasal tip': 'Bulbous nose',
            'prominent lobule of ear':'Large earlobe',
            'tapering fingers':'Tapered finger'
        }
        cell_contents = "Broad forehead, deeply set eyes, ptosis, bulbous nasal tip, micrognathia, prominent lobule of ear, tapering fingers"
        morphMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=morph_d)
        results = morphMapper.map_cell(cell_contents)
        self.assertEqual(7, len(results))
        results = sorted(results, key=lambda x: x.id, reverse=True)
        

        

        
        