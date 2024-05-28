import hpotk
import pytest

from pyphetools.creation import Citation, Disease,Individual, HpTerm



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