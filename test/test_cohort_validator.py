import hpotk
import pytest

from pyphetools.creation import Individual, HpTerm
from pyphetools.validation import CohortValidator


# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"


class TestCohortValidator:

    @pytest.fixture
    def ind_a(self) -> Individual:
        i = Individual(individual_id="A")
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        i.add_hpo_term(HpTerm(hpo_id="HP:0011525", label="Iris nevus"))
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        return i

    @pytest.fixture
    def ind_b(self) -> Individual:
        i = Individual(individual_id="B")
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        i.add_hpo_term(HpTerm(hpo_id="HP:0011525", label="Iris nevus"))
        return i

    def test_redundant_term(
            self,
            hpo: hpotk.Ontology,
            ind_a: Individual,
    ):
        cohort = [ind_a]
        cvalidator = CohortValidator(cohort=cohort, ontology=hpo, min_hpo=1)
        validated_individuals = cvalidator.get_validated_individual_list()
        assert len(validated_individuals) == 1

        vindindividualA = validated_individuals[0]
        assert vindindividualA.has_error()

        errors = vindindividualA.get_validation_errors()
        assert len(errors) == 1

        error = errors[0]
        assert error.error_level == "WARNING"
        assert error.category == "DUPLICATE"
        assert error.message == "<b>Deeply set eye</b> is listed multiple times"
        assert error.term.id == "HP:0000490"
        assert error.term.label == "Deeply set eye"

    def test_no_redundant_term(
            self,
            hpo: hpotk.Ontology,
            ind_b: Individual,
    ):
        cohort = [ind_b]
        cvalidator = CohortValidator(cohort=cohort, ontology=hpo, min_hpo=1)

        validated_individuals = cvalidator.get_validated_individual_list()
        assert len(validated_individuals) == 1

        vindindividualB = validated_individuals[0]
        assert not vindindividualB.has_error()

    def test_redundant_in_hierarchy(self, hpo: hpotk.Ontology):
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
        cvalidator = CohortValidator(cohort=cohort, ontology=hpo, min_hpo=1)
        validated_individuals = cvalidator.get_validated_individual_list()
        assert len(validated_individuals) == 1

        individual_C = validated_individuals[0]
        assert individual_C.has_error()

        errors = individual_C.get_validation_errors()
        assert len(errors) == 1

        error = errors[0]
        assert error.message == "<b>Facial palsy</b> is redundant because of <b>Bilateral facial palsy</b>"
