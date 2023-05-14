import unittest
import os
from pyphetools.creation import HpoParser, CustomColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestCustomColumnMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()

    def test_multiple_items_in_cell_1(self):
        seizure_d = {'Absence': 'Typical absence seizure',
                     'Infantile spasms': "Infantile spasms" ,
                     'GTC': 'Bilateral tonic-clonic seizure' ,
                     'ESES': "Status epilepticus"
                     }
        seizureMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr, custom_map_d=seizure_d)
        results = seizureMapper.map_cell("Absence")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0011147", result.id)
        self.assertEqual("Typical absence seizure", result.label)
        self.assertTrue(result.observed)
        self.assertTrue(result.measured)

    def test_multiple_items_in_cell_2(self):
        seizure_d = {'Absence': 'Typical absence seizure',
                     'Infantile spasms': "Infantile spasms",
                     'GTC': 'Bilateral tonic-clonic seizure',
                     'ESES': "Status epilepticus"}
        seizureMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr, custom_map_d=seizure_d)
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
            'bulbous nasal tip': "Bulbous nose",
            'prominent lobule of ear': "Large earlobe",
            'tapering fingers': "Tapered finger",
        }
        cell_contents = "Broad forehead, deeply set eyes, ptosis, bulbous nasal tip, micrognathia, prominent lobule of ear, tapering fingers"
        morphMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr, custom_map_d=morph_d)
        results = morphMapper.map_cell(cell_contents)
        self.assertEqual(7, len(results))
        results = sorted(results, key=lambda x: x.id, reverse=True)