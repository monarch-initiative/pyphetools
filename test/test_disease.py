import unittest
import pytest

from pyphetools.creation import Disease


class TestDisease(unittest.TestCase):

    def test_eri1(self):
        eri1 = Disease(disease_id='OMIM:608739', disease_label='ERI1-related disease')
        assert 'OMIM:608739' == eri1.id
        assert 'ERI1-related disease' == eri1.label

    def test_raise_exception_id_ws(self):
        with pytest.raises(Exception) as e_info:
            eri1 = Disease(disease_id='OMIM: 608739', disease_label='ERI1-related disease')
        assert str(e_info.value) == 'Malformed disease identifier with white space: "OMIM: 608739"'

    def test_raise_exception_label(self):
        with pytest.raises(Exception) as e_info:
            eri1 = Disease(disease_id='OMIM:608739', disease_label=' ERI1-related disease')
        assert str(e_info.value) == 'Malformed disease label (starts/ends with whitespace): " ERI1-related disease"'

    def test_exception_because_of_stray_tab(self):
        disease_id = "OMIM:616457"
        disease_label = "Developmental and epileptic encephalopathy 50\t616457\tAR\t3\t"
        with pytest.raises(ValueError) as val_error:
            disease = Disease(disease_id=disease_id, disease_label=disease_label)
        assert str(val_error.value) == 'Malformed disease label (contains tabs): "Developmental and epileptic encephalopathy 50	616457	AR	3	"'

