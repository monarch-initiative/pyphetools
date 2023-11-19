import unittest
import os
import pandas as pd
from src.pyphetools.creation import HpoParser, CaseEncoder, MetaData
HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')
import phenopackets as PPkt

# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"


class TestCaseParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        hpparser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls._hpo_cr = hpparser.get_hpo_concept_recognizer()
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199")
        metadata.default_versions_with_hpo(version="2022-05-05")
        age_of_last_examination = "P4Y11M"
        sex = "female"
        cls._parser = CaseEncoder(hpo_cr=cls._hpo_cr,
                                individual_id="A",
                                pmid="PMID:123",
                                age_at_last_exam=age_of_last_examination,
                                sex=sex,
                                metadata=metadata.to_ga4gh())

    def test_chief_complaint(self):
        """
        Expect to get
        HP:0000365 	Hearing impairment 	True 	True
        HP:0001742 	Nasal congestion 	True 	True
        HP:0025267 	Snoring
        """
        vignette = "A 17-mo-old boy presented with progressive nasal obstruction, snoring and hearing loss symptoms when referred to the hospital."
        results = self._parser.add_vignette(vignette=vignette)
        self.assertEqual(3, len(results))
        self.assertTrue(isinstance(results, pd.DataFrame))
        tid = results.loc[(results['id'] == 'HP:0000365')]['id'].values[0]
        self.assertEqual("HP:0000365", tid)

    def test_excluded(self):
        """
        Currently, our text mining does not attempt to detect negation, but users can enter a set of term labels that are excluded
        In this case, He had no nasal obstruction should lead to excluded/Nasal congestion
        """
        vignette = "He had no nasal obstruction and he stated that his smell sensation was intact."
        excluded = set()
        excluded.add("Nasal congestion")
        results = self._parser.add_vignette(vignette=vignette, excluded_terms=excluded)
        self.assertEqual(1, len(results))
        tid = results.loc[(results['id'] == 'HP:0001742')]['id'].values[0]
        self.assertEqual("HP:0001742", tid)
        label = results.loc[(results['id'] == 'HP:0001742')]['label'].values[0]
        self.assertEqual("Nasal congestion", label)
        observed = results.loc[(results['id'] == 'HP:0001742')]['observed'].values[0]
        self.assertFalse(observed)
        measured = results.loc[(results['id'] == 'HP:0001742')]['measured'].values[0]
        self.assertTrue(measured)

    def test_excluded2(self):
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
        encoder = CaseEncoder(hpo_cr=self._hpo_cr, individual_id="id", metadata=metadata.to_ga4gh(), pmid="PMID:1")
        df = encoder.add_vignette(vignette=vignette, excluded_terms=excluded, false_positive=false_positive)
        self.assertEqual(0, len(df))



    def test_phenopacket_id(self):
        """
        Test that we construct the phenopacket ID to include the PMID and the individual id
        """
        ppkt = self._parser.get_phenopacket()
        expected_ppkt_id = "PMID_123_A"
        self.assertEqual(expected_ppkt_id, ppkt.id)


    def test_age_last_exam(self):
        individual = self._parser.get_individual()
        self.assertIsNotNone(individual)
        self.assertIsNotNone(individual.age)
        expected_age = "P4Y11M"
        self.assertEqual(expected_age, individual.age)

    def test_sex(self):
        ppkt = self._parser.get_phenopacket()
        self.assertIsNotNone(ppkt.subject)
        self.assertIsNotNone(ppkt.subject.sex)
        expected_sex = PPkt.Sex.FEMALE
        self.assertEqual(expected_sex, ppkt.subject.sex)


