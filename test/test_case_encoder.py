import hpotk
import pandas as pd
import pytest

import phenopackets as PPkt

from pyphetools.creation import CaseEncoder, MetaData, Citation
from pyphetools.creation import PyPheToolsAge, IsoAge
from pyphetools.creation import HpoConceptRecognizer, HpoExactConceptRecognizer


# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"


class TestCaseParse:

    @pytest.fixture(scope='class')
    def hpo_cr(self, hpo: hpotk.Ontology) -> HpoConceptRecognizer:
        return HpoExactConceptRecognizer.from_hpo(hpo)

    @pytest.fixture
    def case_encoder(self, hpo_cr: HpoConceptRecognizer) -> CaseEncoder:
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199")
        metadata.default_versions_with_hpo(version="2022-05-05")
        age_of_last_examination = IsoAge.from_iso8601("P4Y11M")
        sex = "female"
        citation = Citation(pmid="PMID:123", title="example title")
        return CaseEncoder(
            hpo_cr=hpo_cr,
            individual_id="A",
            citation=citation,
            age_of_onset=age_of_last_examination,
            age_at_last_exam=age_of_last_examination,
            sex=sex,
            metadata=metadata.to_ga4gh(),
        )

    def test_chief_complaint(self, case_encoder: CaseEncoder):
        """
        Expect to get
        HP:0000365 	Hearing impairment 	True 	True
        HP:0001742 	Nasal congestion 	True 	True
        HP:0025267 	Snoring
        """
        vignette = "A 17-mo-old boy presented with progressive nasal obstruction, snoring and hearing loss symptoms when referred to the hospital."
        results = case_encoder.add_vignette(vignette=vignette)

        assert len(results) == 3

        assert isinstance(results, pd.DataFrame)

        tid = results.loc[(results['id'] == 'HP:0000365')]['id'].values[0]
        assert tid == "HP:0000365"

    def test_excluded(self, case_encoder: CaseEncoder):
        """
        Currently, our text mining does not attempt to detect negation, but users can enter a set of term labels that are excluded
        In this case, He had no nasal obstruction should lead to excluded/Nasal congestion
        """
        vignette = "He had no nasal obstruction and he stated that his smell sensation was intact."
        excluded = set()
        excluded.add("Nasal congestion")
        results = case_encoder.add_vignette(vignette=vignette, excluded_terms=excluded)
        assert len(results) == 1

        tid = results.loc[(results['id'] == 'HP:0001742')]['id'].values[0]
        assert tid == "HP:0001742"

        label = results.loc[(results['id'] == 'HP:0001742')]['label'].values[0]
        assert label == "Nasal congestion"

        observed = results.loc[(results['id'] == 'HP:0001742')]['observed'].values[0]
        assert not observed

        measured = results.loc[(results['id'] == 'HP:0001742')]['measured'].values[0]
        assert measured

    def test_excluded2(self, hpo_cr: HpoConceptRecognizer):
        """
        The goal if this test is to ensure that 'Seizure' is annotated as 'excluded'
        We label the word as false positive and it should just be skipped
        """
        vignette = "The patient is not on seizure medication at this time."
        excluded = set()
        false_positive = set()
        false_positive.add("seizure")
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199")
        metadata.default_versions_with_hpo(version="2022-05-05")
        citation = Citation(pmid="PMID:1", title="excluded")
        encoder = CaseEncoder(hpo_cr=hpo_cr, individual_id="id", metadata=metadata.to_ga4gh(), citation=citation)
        df = encoder.add_vignette(vignette=vignette, excluded_terms=excluded, false_positive=false_positive)

        assert len(df) == 0



    def test_phenopacket_id(self, case_encoder: CaseEncoder):
        """
        Test that we construct the phenopacket ID to include the PMID and the individual id
        """
        ppkt = case_encoder.get_phenopacket()
        assert ppkt.id == "PMID_123_A"


    def test_age_last_exam(self, case_encoder: CaseEncoder):
        individual = case_encoder.get_individual()
        assert individual is not None
        assert individual.age_of_onset is not None

        expected_age = "P4Y11M"
        onset_age = individual.age_of_onset
        assert onset_age is not None

        assert isinstance(onset_age, PyPheToolsAge)
        assert onset_age.age_string == expected_age

    def test_sex(self, case_encoder: CaseEncoder):
        ppkt = case_encoder.get_phenopacket()
        assert ppkt.subject is not None
        assert ppkt.subject.sex is not None

        expected_sex = PPkt.Sex.FEMALE
        assert ppkt.subject.sex == expected_sex


