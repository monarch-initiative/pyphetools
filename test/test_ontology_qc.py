import hpotk
import pytest

from pyphetools.creation import HpTerm, Individual, IsoAge
from pyphetools.validation import OntologyQC




class TestOntologyQC:

    @pytest.fixture
    def ontology_qc(self, hpo: hpotk.Ontology) -> OntologyQC:
        individual = Individual(individual_id="id")
        return OntologyQC(ontology=hpo, individual=individual)


    def test_conflict(self, hpo: hpotk.Ontology):
        """
        Arachnodactyly is a child of Slender finger, and so the following is a conflict
        """
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=False)
        hpo_terms = [arachTerm, slenderTerm]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)

        qc = OntologyQC(ontology=hpo, individual=individual)

        qc_hpo_terms = qc.get_clean_terms()
        assert len(qc_hpo_terms) == 1

    def test_do_not_detect_conflict_if_there_is_no_conflict(self, hpo: hpotk.Ontology):
        """
        These terms are unrelated so it is NOT a conflict
        """
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        # the following is not a conflict and should not be removed
        hipDislocation = HpTerm(hpo_id="HP:0002827", label="Hip dislocation", observed=False)
        hpo_terms = [arachTerm, hipDislocation]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)

        qc = OntologyQC(ontology=hpo, individual=individual)
        qc_hpo_terms = qc.get_clean_terms()

        assert len(qc_hpo_terms) == 2

    def test_do_not_detect_conflict_if_there_is_no_conflict_2(self, hpo: hpotk.Ontology):
        """
        This is not a conflict because the subclass is excluded while the superclass is observed
        """
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=False)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=True)
        hpo_terms = [arachTerm, slenderTerm]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)
        qc = OntologyQC(ontology=hpo, individual=individual)
        qc_hpo_terms = qc.get_clean_terms()
        assert len(qc_hpo_terms) == 2

    def test_redundancy(self, hpo: hpotk.Ontology):
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        slenderTerm = HpTerm(hpo_id="HP:0001238", label="Slender finger", observed=True)
        hpo_terms = [arachTerm, slenderTerm]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)
        qc = OntologyQC(ontology=hpo, individual=individual)
        qc_hpo_terms = qc.get_clean_terms()

        assert len(qc_hpo_terms) == 1

    def test_do_not_remove_if_not_redundant(self, hpo: hpotk.Ontology):
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        hipDislocation = HpTerm(hpo_id="HP:0002827", label="Hip dislocation", observed=False)
        hpo_terms = [arachTerm, hipDislocation]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)
        qc = OntologyQC(ontology=hpo, individual=individual)
        qc_hpo_terms = qc.get_clean_terms()

        assert len(qc_hpo_terms) == 2


    def test_exact_redundancy(self, hpo: hpotk.Ontology):
        arachTerm = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        arachTerm2 = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        hipDislocation = HpTerm(hpo_id="HP:0002827", label="Hip dislocation", observed=False)
        hpo_terms = [arachTerm, arachTerm2, hipDislocation]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)
        qc = OntologyQC(ontology=hpo, individual=individual)
        qc_hpo_terms = qc.get_clean_terms()

        assert len(qc_hpo_terms) == 2

        error_list = qc.get_error_list()

        assert len(error_list) == 1

        error = error_list[0]

        assert error.error_level == 'WARNING'
        assert error.category == 'DUPLICATE'


    def test_same_term_observed_and_excluded(self, hpo: hpotk.Ontology):
        arachTermObserved = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=True)
        arachTermExcluded = HpTerm(hpo_id="HP:0001166", label="Arachnodactyly", observed=False)
        hipDislocation = HpTerm(hpo_id="HP:0002827", label="Hip dislocation", observed=True)
        hpo_terms = [arachTermObserved, hipDislocation, arachTermExcluded]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)
        qc = OntologyQC(ontology=hpo, individual=individual)
        error_list = qc.get_error_list()

        assert len(error_list) == 1

        error = error_list[0]

        assert error.error_level == "ERROR"
        assert error.category == "OBSERVED_AND_EXCLUDED"
        assert error.message == "Term Arachnodactyly (HP:0001166) was annotated to be both observed and excluded."

    def test_redundancy_with_and_without_onset(self, hpo: hpotk.Ontology):
        """
        If we have Myoclonic seizure with onset P1Y and Seizure with no onset, then we do not want to include
        Seizure in the final output because it is redundant.
        Myoclonic seizure HP:0032794 ("grandchild" of Seizure)
        Seizure HP:0001250
        """
        onset = IsoAge.from_iso8601("P1Y")
        myoclonic_seiz = HpTerm(hpo_id="HP:0032794", label="Myoclonic seizure", observed=True, onset=onset)
        seiz = HpTerm(hpo_id="HP:0001250", label="Seizure", observed=True)
        hpo_terms = [myoclonic_seiz, seiz]
        individual = Individual(individual_id="id", hpo_terms=hpo_terms)

        qc = OntologyQC(ontology=hpo, individual=individual)

        qc_hpo_terms = qc.get_clean_terms()

        assert len(qc_hpo_terms) == 1
