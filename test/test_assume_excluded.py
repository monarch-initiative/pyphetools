import os
import unittest

from pyphetools.creation import HpoParser, OptionColumnMapper

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
        comorbiditiesMapper = OptionColumnMapper(column_name="placeholder",
                                                concept_recognizer=self.hpo_cr,
                                                option_d=comorbidities_d)
        results = comorbiditiesMapper.map_cell('COPD')
        self.assertEqual(1, len(results))
        hpo_term = results[0]
        self.assertEqual('Chronic pulmonary obstruction', hpo_term.label)
        self.assertEqual('HP:0006510', hpo_term.id)

    def test_with_assume_exclusion(self):
        excluded_d = {'Insulindependentdiabetes-onsetatage19': 'Type II diabetes mellitus',
                            'COPD': 'Chronic pulmonary obstruction',
                            'Diastolicdysfunction': 'Left ventricular diastolic dysfunction',
                            'Lymphocytosis': 'Lymphocytosis',
                            'Single kidney': 'Unilateral renal agenesis'}
        comorbiditiesMapper = OptionColumnMapper(column_name="placeholder", concept_recognizer=self.hpo_cr, option_d={}, excluded_d=excluded_d)
        results = comorbiditiesMapper.map_cell('COPD')
        self.assertEqual(1, len(results))
        hpo0 = results[0]
        self.assertEqual('Chronic pulmonary obstruction', hpo0.label)
        self.assertEqual('HP:0006510', hpo0.id)
        self.assertFalse(hpo0.observed)
        results = comorbiditiesMapper.map_cell('Diastolicdysfunction')
        hpo1 = results[0]
        self.assertEqual("Left ventricular diastolic dysfunction", hpo1.label)
        self.assertEqual("HP:0025168", hpo1.id)
        self.assertFalse(hpo1.observed)
        results = comorbiditiesMapper.map_cell('Lymphocytosis')
        hpo2 = results[0]
        self.assertEqual("Lymphocytosis", hpo2.label)
        self.assertFalse(hpo2.observed)
        results = comorbiditiesMapper.map_cell('Insulindependentdiabetes-onsetatage19')
        hpo3 = results[0]
        self.assertEqual("Type II diabetes mellitus", hpo3.label)
        self.assertFalse(hpo3.observed)
        results = comorbiditiesMapper.map_cell('Single kidney')
        hpo4 = results[0]
        self.assertEqual("Unilateral renal agenesis", hpo4.label)
        self.assertFalse(hpo4.observed)
