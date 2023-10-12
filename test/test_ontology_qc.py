import unittest
import os
from src.pyphetools.creation import HpoToolkitParser, OntologyQC, HpTerm


HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestOntologyQC(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoToolkitParser(hpo_json_file=HP_JSON_FILENAME)
        hpo_cr = parser.get_hpo_concept_recognizer()
        ontology = hpo_cr.get_hpo_ontology()
        cls._qc = OntologyQC(ontology=ontology)

    def test_non_null(self):
        self.assertIsNotNone(self._qc)

    def test_conflict(self):
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=False)
        hpo_terms = [arachTerm, slenderTerm]
        qc_hpo_terms = self._qc.clean_terms(hpo_terms)
        self.assertEqual(1, len(qc_hpo_terms))
