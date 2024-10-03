import pytest

from pyphetools.visualization import DiseaseSpecificHpoCounter, HpoCohortCount
from pyphetools.pp.v202 import OntologyClass as OntologyClass202

class TestDiseaseSpecificHpoCounter:

    def test_HpoCohortCount(self):
        oclzz = OntologyClass202(id="HP:0001288", label="Gait disturbance")
        eri1 = OntologyClass202(id='OMIM:608739', label='ERI1-related disease')
        eri2 = OntologyClass202(id='OMIM:608742', label='ERI2-related disease') # fake
        eri3 = OntologyClass202(id='OMIM:608744', label='ERI3-related disease') # fake
        hpo_counter = HpoCohortCount(hpo=oclzz)
        assert hpo_counter is not None
        hpo_counter.increment_observed(eri1)
        assert hpo_counter.get_observed(eri1) == 1
        hpo_counter.increment_observed(eri1)
        hpo_counter.increment_observed(eri1)
        assert hpo_counter.get_observed(eri1) == 3
        hpo_counter.increment_excluded(eri1)
        assert hpo_counter.get_observed(eri1) == 3
        assert hpo_counter.get_excluded(eri1) == 1
        hpo_counter.increment_observed(eri2)
        hpo_counter.increment_observed(eri2)
        hpo_counter.increment_excluded(eri2)
        hpo_counter.increment_excluded(eri2)
        hpo_counter.increment_excluded(eri2)
        assert hpo_counter.get_observed(eri2) == 2
        assert hpo_counter.get_excluded(eri2) == 3
        assert hpo_counter.get_observed(eri1) == 3
        assert hpo_counter.get_excluded(eri1) == 1
        assert hpo_counter.get_observed(eri3) == 0 ## we did not add frequencies for this disease
        assert hpo_counter.frequency_for_disease(eri1) == "3/4 (75%)"
        assert hpo_counter.frequency_for_disease(eri2) == "2/5 (40%)"
        assert hpo_counter.frequency_for_disease(eri3) == "n/a" # no information available for eri3
        assert hpo_counter.get_maximum_frequency() == 0.75


