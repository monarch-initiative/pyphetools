import unittest
import os
from src.pyphetools.creation import HpoParser, OntologyQC, HpTerm


HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestOntologyQC(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        hpo_cr = parser.get_hpo_concept_recognizer()
        ontology = hpo_cr.get_hpo_ontology()
        cls._qc = OntologyQC(ontology=ontology)

    def test_non_null(self):
        self.assertIsNotNone(self._qc)

    def test_conflict(self):
        """
        Arachnodactyly is a child of Slender finger, and so the following is a conflict
        """
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=False)
        hpo_terms = [arachTerm, slenderTerm]
        qc_hpo_terms = self._qc.clean_terms(hpo_terms)
        self.assertEqual(1, len(qc_hpo_terms))

    def test_do_not_detect_conflict_if_there_is_no_conflict(self):
        """
        These terms are unrelated so it is NOT a conflict
        """
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        # the following is not a conflict and should not be removed
        hipDislocation = HpTerm(hpo_id="HP:0002827", label="Hip dislocation", observed=False)
        hpo_terms = [arachTerm, hipDislocation]
        qc_hpo_terms = self._qc.clean_terms(hpo_terms)
        self.assertEqual(2, len(qc_hpo_terms))

    def test_do_not_detect_conflict_if_there_is_no_conflict_2(self):
        """
        This is not a conflict because the subclass is excluded while the superclass is observed
        """
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=False)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=True)
        hpo_terms = [arachTerm, slenderTerm]
        qc_hpo_terms = self._qc.clean_terms(hpo_terms)
        self.assertEqual(2, len(qc_hpo_terms))

    def test_redundancy(self):
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=True)
        hpo_terms = [arachTerm, slenderTerm]
        qc_hpo_terms = self._qc.clean_terms(hpo_terms)
        self.assertEqual(1, len(qc_hpo_terms))

    def test_do_not_remove_if_not_redundant(self):
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        hipDislocation = HpTerm(hpo_id="HP:0002827", label="Hip dislocation", observed=False)
        hpo_terms = [arachTerm, hipDislocation]
        qc_hpo_terms = self._qc.clean_terms(hpo_terms)
        self.assertEqual(2, len(qc_hpo_terms))

