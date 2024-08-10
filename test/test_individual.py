import hpotk
import pytest

from pyphetools.creation import Citation, Disease,Individual, HpTerm
from pyphetools.pp.v202 import VitalStatus, TimeElement, Age, OntologyClass



# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"


class TestIndividual:

    @pytest.fixture
    def ind_a(self) -> Individual:
        cite = Citation(pmid="PMID:1234", title="some title")
        i = Individual(individual_id="Individual A (from previous publication)", citation=cite)
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        i.set_disease(disease=Disease(disease_id="OMIM:123456", disease_label="label"))
        return i
    
    @pytest.fixture
    def ind_b(self) -> Individual:
        cite = Citation(pmid="PMID:36446582", title="some title")
        i = Individual(individual_id="Alves, 2019", citation=cite)
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        i.set_disease(disease=Disease(disease_id="OMIM:123456", disease_label="label"))
        return i
    
    @pytest.fixture
    def ind_c(self) -> Individual:
        cite = Citation(pmid="PMID:36446582", title="some title")
        i = Individual(individual_id="Low, 2016_P17 (10)", citation=cite)
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        i.set_disease(disease=Disease(disease_id="OMIM:123456", disease_label="label"))
        return i
    
    @pytest.fixture
    def ind_d(self) -> Individual:
        cite = Citation(pmid="PMID:36446582", title="some title")
        time_at_last_encounter=TimeElement(
            element=Age(
                iso8601duration='P6M',
            )
        )
        vital_status=VitalStatus(
            status=VitalStatus.Status.DECEASED,
            time_of_death=TimeElement(element=Age(iso8601duration='P1Y')),
            cause_of_death=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            survival_time_in_days=180,
        )
        i = Individual(individual_id="Low, 2016_P17 (10)", age_at_last_encounter=time_at_last_encounter, vital_status=vital_status, citation=cite)
        i.add_hpo_term(HpTerm(hpo_id="HP:0000490", label="Deeply set eye"))
        i.set_disease(disease=Disease(disease_id="OMIM:123456", disease_label="label"))
        return i


    
    
    def test_phenopacket_identifier(
            self,
            ind_a: Individual,
    ):
        phenopacket_id = ind_a.get_phenopacket_id()
        expected = "PMID_1234_Individual_A_from_previous_publication"
        assert expected == phenopacket_id


    def test_phenopacket_id_B(self, ind_b: Individual):
        phenopacket_id = ind_b.get_phenopacket_id()
        expected = "PMID_36446582_Alves_2019"
        assert expected == phenopacket_id

    def test_phenopacket_id_C(self, ind_c: Individual):
        phenopacket_id = ind_c.get_phenopacket_id()
        expected = "PMID_36446582_Low_2016_P17_10"
        assert expected == phenopacket_id

    def test_phenopacket_vital_status(self, ind_d: Individual):
        vstat = ind_d.get_vital_status()
        assert vstat is not None
        assert vstat.status == VitalStatus.Status.DECEASED
        assert 180 == vstat.survival_time_in_days
        #  cause_of_death=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
        assert "NCIT:C7541" == vstat.cause_of_death.id
        assert "Retinoblastoma" == vstat.cause_of_death.label

    def test_phenopacket_last_encounter(self, ind_d: Individual):
        last_encounter = ind_d.age_at_last_encounter
        assert last_encounter is not None 
        assert last_encounter.age is not None
        assert last_encounter.age_range is None 
        age = last_encounter.age
        assert age.iso8601duration == "P6M"
