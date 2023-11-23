import os
import unittest

from src.pyphetools.creation import Individual, HpTerm, HpoParser
from src.pyphetools.validation import CohortValidator
from src.pyphetools.validation.validation_result import ErrorLevel, Category

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')

# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')

class TestCohortValidator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        individual_A = Individual(individual_id="A")
        individual_A.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        individual_A.add_hpo_term(HpTerm(hpo_id="HP:0011525", label="Iris nevus"))
        individual_A.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        individual_B = Individual(individual_id="B")
        individual_B.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        individual_B.add_hpo_term(HpTerm(hpo_id="HP:0011525", label="Iris nevus"))
        cls._individual_A = individual_A
        cls._individual_B = individual_B
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()


    def test_redundant_term(self):
        cohort = [self._individual_A]
        hpo_ontology = self.hpo_cr.get_hpo_ontology()
        cvalidator = CohortValidator(cohort=cohort, ontology=hpo_ontology, min_hpo=1)
        validated_individuals = cvalidator.get_validated_individual_list()
        self.assertEqual(1, len(validated_individuals))
        vindindividualA = validated_individuals[0]
        self.assertTrue(vindindividualA.has_error())
        errors = vindindividualA.get_validation_errors()
        self.assertEqual(1, len(errors))
        error = errors[0]
        self.assertEqual("WARNING", error.error_level)
        self.assertEqual("REDUNDANT", error.category)
        self.assertEqual("<b>Deeply set eye</b> is listed multiple times", error.message)
        self.assertEqual("HP:0000490", error.term.id)
        self.assertEqual("Deeply set eye", error.term.label)

    def test_no_redundant_term(self):
        cohort = [self._individual_B]
        hpo_ontology = self.hpo_cr.get_hpo_ontology()
        cvalidator = CohortValidator(cohort=cohort, ontology=hpo_ontology, min_hpo=1)
        validated_individuals = cvalidator.get_validated_individual_list()
        self.assertEqual(1, len(validated_individuals))
        vindindividualB = validated_individuals[0]
        self.assertFalse(vindindividualB.has_error())

    def test_redundant_in_hierarchy(self):
        """
        0358596_patientA.json,ERROR,HpoAncestryValidator,Violation of the annotation propagation rule,
        "Phenotypic features of PMID_20358596_patient_A must not contain both an
        observed term (Bilateral facial palsy, HP:0430025) and an observed ancestor (Facial palsy, HP:0010628)"
        """
        individual_C = Individual(individual_id="C")
        individual_C.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        individual_C.add_hpo_term(HpTerm(hpo_id="HP:0011525", label="Iris nevus"))
        individual_C.add_hpo_term(HpTerm(hpo_id="HP:0430025", label="Bilateral facial palsy"))
        individual_C.add_hpo_term(HpTerm(hpo_id="HP:0010628", label="Facial palsy"))
        cohort = [individual_C]
        hpo_ontology = self.hpo_cr.get_hpo_ontology()
        cvalidator = CohortValidator(cohort=cohort, ontology=hpo_ontology, min_hpo=1)
        validated_individuals = cvalidator.get_validated_individual_list()
        self.assertEqual(1, len(validated_individuals))
        individual_C = validated_individuals[0]
        self.assertTrue(individual_C.has_error())
        errors = individual_C.get_validation_errors()
        self.assertEqual(1, len(errors))
        error = errors[0]
        self.assertEqual("<b>Facial palsy</b> is redundant because of <b>Bilateral facial palsy</b>", error.message)

