import pytest

from pyphetools.creation import Measurements
from pyphetools.pp.v202 import Measurement as Measurement202

class TestMeasurements:

    def test_nanogram_per_milliliter(self):
        lower_limit_of_normal = 0
        upper_limit_of_normal = 25 ## ng/ml
        concentration = 40
        measurement = Measurements.nanogram_per_milliliter(code="LOINC:2842-3",
                                      label="Prolactin [Mass/Vol]",
                                      concentration=concentration,
                                      low=lower_limit_of_normal,
                                      high=upper_limit_of_normal)
        assert isinstance(measurement, Measurement202)
        assert measurement.assay.id == "LOINC:2842-3"
        assert measurement.assay.label == "Prolactin [Mass/Vol]"
        assert measurement.value.value.value == concentration
        refrange = measurement.value.value.reference_range
        assert refrange is not None
        assert refrange.low == lower_limit_of_normal
        assert refrange.high == upper_limit_of_normal


 