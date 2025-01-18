import unittest
import pytest
from pyphetools.creation import PyPheToolsAge
from pyphetools.pp.v202 import TimeElement as TimeElement202


class TestSimpleAge(unittest.TestCase):
    #'age_of_onset': 'Infantile onset', 'age_at_last_encounter': 'P3Y9M', 'sex': 'M'}
    def test_infantile_onset(self):
        onset_age = PyPheToolsAge.get_age_pp201('Infantile onset')
        self.assertIsNotNone(onset_age)
        self.assertEqual('Infantile onset', onset_age.ontology_class.label)
        self.assertTrue(isinstance(onset_age, TimeElement202))

    def test_3m9m(self):
        onset_age = PyPheToolsAge.get_age_pp201('P3Y9M')
        self.assertIsNotNone(onset_age)
        self.assertEqual('P3Y9M', onset_age.age.iso8601duration)
        self.assertTrue(isinstance(onset_age, TimeElement202))

    def test_2m(self):
        onset_age = PyPheToolsAge.get_age_pp201('P2M')
        self.assertIsNotNone(onset_age)
        self.assertEqual('P2M', onset_age.age.iso8601duration)
        self.assertTrue(isinstance(onset_age, TimeElement202))

    def test_malformed_6M(self):
        """
        A common error is P0.5Y, which should be P6M. This should throw an Exception
        """
        with pytest.raises(ValueError, match="Invalid ISO8601 expression: 'P0.5Y'") as excinfo:
            onset_age = PyPheToolsAge.get_age_pp201('P0.5Y')
        assert "Invalid ISO8601 expression: 'P0.5Y'" == str(excinfo.value)


    def test_age_key_converter_iso(self):
        time_elem202 = PyPheToolsAge.get_age_pp201("P41Y")
        assert time_elem202 is not None
        assert time_elem202.age
        assert time_elem202.age.iso8601duration == "P41Y"

    def test_age_key_converter_hpterm(self):
        time_elem202 = PyPheToolsAge.get_age_pp201("Congenital onset")
        assert time_elem202 is not None
        assert not time_elem202.age
        assert time_elem202.ontology_class
        oterm = time_elem202.ontology_class
        assert oterm.id == "HP:0003577"
        assert oterm.label == "Congenital onset"

    def test_malformed_key_converter(self):
        with pytest.raises(ValueError) as verror:
            time_elem = PyPheToolsAge.get_age_pp201("MALFORMED LABEL")
