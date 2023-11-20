import os
import unittest

from src.pyphetools.creation import HpoParser

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestOptionMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()

    def test_mixed(self):
        cell_contents = "Long and thick eyebrows, upper slanted palpebral fissures, anteverted nares, short philtrum"
        other_d = {'upper slanted palpebral fissures': 'Upslanted palpebral fissure'}
        results = self.hpo_cr.parse_cell(cell_contents=cell_contents, custom_d=other_d)
        # sort results in order of HP ids for testing
        # We expect
        # Thick eyebrow (HP:0000574)
        # Upslanted palpebral fissure (HP:0000582)
        # Anteverted nares (HP:0000463)
        # Short philtrum (HP:0000322)
        results = sorted(results, key=lambda x: x.id)
        self.assertEqual(4, len(results))
        self.assertEqual("HP:0000322", results[0].id)
        self.assertEqual("Short philtrum", results[0].label)
        self.assertTrue(results[0].observed)
        self.assertTrue(results[0].measured)
        self.assertEqual("HP:0000463", results[1].id)
        self.assertEqual("Anteverted nares", results[1].label)
        self.assertTrue(results[1].observed)
        self.assertTrue(results[1].measured)
        self.assertEqual("HP:0000574", results[2].id)
        self.assertEqual("Thick eyebrow", results[2].label)
        self.assertTrue(results[2].observed)
        self.assertTrue(results[2].measured)
        self.assertEqual("HP:0000582", results[3].id)
        self.assertEqual("Upslanted palpebral fissure", results[3].label)
        self.assertTrue(results[3].observed)
        self.assertTrue(results[3].measured)

    def test_mixed_2(self):
        morph_d = {
            'bulbous nasal tip': 'Bulbous nose',
            'prominent lobule of ear': 'Large earlobe',
            'tapering fingers': 'Tapered finger',
            'deeply set eyes': "Deeply set eye" # Note this synonym is not yet in HPO version used for testing
        }
        cell_contents = "Broad forehead, deeply set eyes, ptosis, bulbous nasal tip, micrognathia, prominent lobule of ear, tapering fingers"
        results = self.hpo_cr.parse_cell(cell_contents=cell_contents, custom_d=morph_d)
        # Expect
        # Broad forehead (HP:0000337)
        # Micrognathia (HP:0000347)
        # Bulbous nose (HP:0000414)
        # Deeply set eye (HP:0000490)
        # Ptosis (HP:0000508)
        # Tapered finger (HP:0001182)
        # Large earlobe (HP:0009748)
        self.assertEqual(7, len(results))
        results = sorted(results, key=lambda x: x.id)
        self.assertEqual("HP:0000337", results[0].id)
        self.assertEqual("Broad forehead", results[0].label)
        self.assertTrue(results[0].observed)
        self.assertTrue(results[0].measured)
        self.assertEqual("HP:0000347", results[1].id)
        self.assertEqual("Micrognathia", results[1].label)
        self.assertEqual("HP:0000414", results[2].id)
        self.assertEqual("Bulbous nose", results[2].label)
        self.assertEqual("HP:0000490", results[3].id)
        self.assertEqual("Deeply set eye", results[3].label)
        self.assertEqual("HP:0000508", results[4].id)
        self.assertEqual("Ptosis", results[4].label)
        self.assertEqual("HP:0001182", results[5].id)
        self.assertEqual("Tapered finger", results[5].label)
        self.assertEqual("HP:0009748", results[6].id)
        self.assertEqual("Large earlobe", results[6].label)

    def test_pair_of_custom_concepts(self):
        seizure_d = {'Absence': 'Typical absence seizure',
                     'Infantile spasms': 'Infantile spasms',
                     'GTC': 'Bilateral tonic-clonic seizure',
                     'ESES': 'Status epilepticus'}
        cell_contents = "Absence and GTC"
        results = self.hpo_cr.parse_cell(cell_contents=cell_contents, custom_d=seizure_d)
        ## Expect
        # Typical absence seizure (HP:0011147)
        # Bilateral tonic-clonic seizure (HP:0002069)
        self.assertEqual(2, len(results))
        results = sorted(results, key=lambda x: x.id)
        self.assertEqual("HP:0002069", results[0].id)
        self.assertEqual("Bilateral tonic-clonic seizure", results[0].label)
        self.assertTrue(results[0].observed)
        self.assertTrue(results[0].measured)
        self.assertEqual("HP:0011147", results[1].id)
        self.assertEqual("Typical absence seizure", results[1].label)
        self.assertTrue(results[1].observed)
        self.assertTrue(results[1].measured)

    def test_get_longest_overlapping(self):
        cell_contents = "Cryptorchidism, micropenis, bilateral talipes equinovarus"
        results_longest = self.hpo_cr.parse_cell(cell_contents=cell_contents)
        label_set = {result.label for result in results_longest}
        self.assertIn("Cryptorchidism", label_set, "Could not find Cryptorchidism in results")
        self.assertIn("Micropenis", label_set, "Could not find Micropenis in results")
        self.assertEqual(3, len(label_set))

    def test_initialize_cr(self):
        items = {
            'regression': ["Developmental regression", "HP:0002376"],
            'autism': ['Autism', 'HP:0000717'],
            'hypotonia': ['Hypotonia', 'HP:0001252'],
            'movement disorder': ['Abnormality of movement', 'HP:0100022'],
            'CVI': ['Cerebral visual impairment', 'HP:0100704'],  # CVI stands for Cortical visual impairment HP:0100704
            'seizures': ['Seizure', 'HP:0001250']
        }
        item_column_mapper_d = self.hpo_cr.initialize_simple_column_maps(column_name_to_hpo_label_map=items,
                                                                         observed='yes',
                                                                         excluded='no')
        self.assertEqual(6, len(item_column_mapper_d))


    def test_pica_not_at_boundary(self):
        """
        We do not want Pica HP:0011856 to match with typical
        loss of typical trabecular bony architecture
        """
        cell_contents = "loss of typical trabecular bony architecture"
        results = self.hpo_cr.parse_cell(cell_contents=cell_contents)
        self.assertEqual(0, len(results))

    def test_pica(self):
        """
        This should match
        """
        cell_contents = "Pica is a condition where a person compulsively swallows non-food items."
        results = self.hpo_cr.parse_cell(cell_contents=cell_contents)
        self.assertEqual(1, len(results))



