import unittest
import os
from src.pyphetools.creation import HpoParser, OptionColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestAssumeExcluded(unittest.TestCase):
    """
    This test class checks the function of the assumeExcluded argument of the OptionColumnMapper.
    """

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        cls.severity_d = {'mild': 'Intellectual disability, mild',
                        'moderate': 'Intellectual disability, moderate',
                        'severe': 'Intellectual disability, severe'
                        }


    def test_without_assume_exclusion(self):
        comorbidities_d = {'Insulindependentdiabetes-onsetatage19': 'Type II diabetes mellitus',
                            'COPD': 'Chronic pulmonary obstruction',
                            'Diastolicdysfunction': 'Left ventricular diastolic dysfunction',
                            'Lymphocytosis': 'Lymphocytosis',
                            'Single kidney': 'Unilateral renal agenesis'}
        comorbiditiesMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=comorbidities_d)
        results = comorbiditiesMapper.map_cell('COPD')
        self.assertEqual(1, len(results))
        hpo_term = results[0]
        self.assertEqual('Chronic pulmonary obstruction', hpo_term.label)
        self.assertEqual('HP:0006510', hpo_term.id)

    def test_with_assume_exclusion(self):
        comorbidities_d = {'Insulindependentdiabetes-onsetatage19': 'Type II diabetes mellitus',
                            'COPD': 'Chronic pulmonary obstruction',
                            'Diastolicdysfunction': 'Left ventricular diastolic dysfunction',
                            'Lymphocytosis': 'Lymphocytosis',
                            'Single kidney': 'Unilateral renal agenesis'}
        comorbiditiesMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=comorbidities_d, assumeExcluded=True)
        results = comorbiditiesMapper.map_cell('COPD')
        self.assertEqual(5, len(results))
        results.sort(key=lambda x: x.label) # sort alphabetically
        hpo0 = results[0]
        self.assertEqual('Chronic pulmonary obstruction', hpo0.label)
        self.assertEqual('HP:0006510', hpo0.id)
        self.assertTrue(hpo0.observed)
        hpo1 = results[1]
        self.assertEqual("Left ventricular diastolic dysfunction", hpo1.label)
        self.assertEqual("HP:0025168", hpo1.id)
        self.assertFalse(hpo1.observed)
        hpo2 = results[2]
        self.assertEqual("Lymphocytosis", hpo2.label)
        self.assertFalse(hpo2.observed)
        hpo3 = results[3]
        self.assertEqual("Type II diabetes mellitus", hpo3.label)
        self.assertFalse(hpo3.observed)
        hpo4 = results[4]
        self.assertEqual("Unilateral renal agenesis", hpo4.label)
        self.assertFalse(hpo4.observed)
