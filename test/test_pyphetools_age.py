import unittest
from pyphetools.creation import PyPheToolsAge, HpoAge, IsoAge


class TestSimpleAge(unittest.TestCase):
    #'age_of_onset': 'Infantile onset', 'age_at_last_encounter': 'P3Y9M', 'sex': 'M'}
    def test_infantile_onset(self):
        onset_age = PyPheToolsAge.get_age('Infantile onset')
        self.assertIsNotNone(onset_age)
        self.assertEqual('Infantile onset', onset_age.age_string)
        self.assertTrue(isinstance(onset_age, HpoAge))

    def test_3m9m(self):
        onset_age = PyPheToolsAge.get_age('P3Y9M')
        self.assertIsNotNone(onset_age)
        self.assertEqual('P3Y9M', onset_age.age_string)
        self.assertTrue(isinstance(onset_age, IsoAge))

    def test_2m(self):
        onset_age = PyPheToolsAge.get_age('P2M')
        self.assertIsNotNone(onset_age)
        self.assertEqual('P2M', onset_age.age_string)
        self.assertTrue(isinstance(onset_age, IsoAge))
