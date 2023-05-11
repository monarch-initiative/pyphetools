import unittest
import os
from pyphetools.creation import HpoParser, CustomColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestCustomColumnMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()

    def test_hpo_cr_non_null(self):
        """sanity check"""
        self.assertIsNotNone(self.hpo_cr)

    def test_hpo_cr_ataxia(self):
        """We should retrieve Ataxia (HP:0001251)"""
        neuroMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr)
        results = neuroMapper.map_cell("ataxia")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0001251", result.id)
        self.assertEqual("Ataxia", result.label)

    def test_hpo_cr_spastic_paraplegia(self):
        """We should retrieve Spastic paraplegia (HP:0001258)"""
        neuroMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr)
        results = neuroMapper.map_cell("spastic paraplegia")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0001258", result.id)
        self.assertEqual("Spastic paraplegia", result.label)

    def test_hpo_cr_multiple_concepts_with_custom_map(self):
        text = 'spasticity; nerve conduction and EMG studies with abnormal findings "remarkable for the failure to activate the leg muscles due to an upper motor neuron pattern of aberrant motor unit potential firing rates. These findings are consistent with dysfunction of the corticospinal pathways rather than a lower motor unit."'
        neuroMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr)
        results = neuroMapper.map_cell(text)
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0001257", result.id)
        self.assertEqual("Spasticity", result.label)

    def test_hpo_cr_multiple_concepts_no_custom_map(self):
        text = 'spasticity; nerve conduction and EMG studies with abnormal findings "remarkable for the failure to activate the leg muscles due to an upper motor neuron pattern of aberrant motor unit potential firing rates. These findings are consistent with dysfunction of the corticospinal pathways rather than a lower motor unit." Significant low extremity weakness.'
        neuro_exam_custom_map = {'low extremity weakness': 'Lower limb muscle weakness',
                                 'unstable gait': 'Unsteady gait',
                                 'dysfunction of the corticospinal pathways': 'Upper motor neuron dysfunction',
                                 }
        neuroMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr, custom_map_d=neuro_exam_custom_map)
        results = neuroMapper.map_cell(text)
        self.assertEqual(3, len(results))
        term_d = dict([(hpo_term.id, hpo_term.label) for hpo_term in results])
        self.assertTrue("HP:0001257" in term_d)
        self.assertEqual("Spasticity", term_d.get("HP:0001257"))
        self.assertTrue("HP:0007340" in term_d)
        self.assertEqual("Lower limb muscle weakness", term_d.get("HP:0007340"))
        self.assertTrue("HP:0002493" in term_d)
        self.assertEqual("Upper motor neuron dysfunction", term_d.get("HP:0002493"))

    def test_SETD2(self):
        text = """Extra fluid in the back of the cerebellum at 35 weeks; fetal MRI at 35 weeks showed VSD, 
        small cerebellum, and agenesis of the corpus callosum; pre-eclampsia; \nIUGR 	n/a """
        prenatal_custom_map = {'agenesis of the corpus callosum': 'Agenesis of corpus callosum',
                               '\nIUGR': 'Intrauterine growth retardation',
                               'small cerebellum': 'Cerebellar hypoplasia',
                               }
        prenatalMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr, custom_map_d=prenatal_custom_map)
        results = prenatalMapper.map_cell(text)
        self.assertEqual(3, len(results))

    def test_get_maximal_match(self):
        text = "severe global developmental delay"
        dev_custom_map = {'Severe global developmental delay': 'Severe global developmental delay'}
        devMapper = CustomColumnMapper(concept_recognizer=self.hpo_cr, custom_map_d=dev_custom_map)
        results = devMapper.map_cell(text)
        self.assertEqual(1, len(results))
        res = results[0]
        self.assertEqual(res.label, "Severe global developmental delay")
