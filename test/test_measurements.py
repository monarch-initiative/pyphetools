import pytest

from pyphetools.creation import Measurements
from pyphetools.pp.v202 import Measurement as Measurement202

from src.pyphetools.pp.v202 import OntologyClass


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


    def test_percent(self):
        loinc_code = "LOINC:74892-1"
        loinc_label = "Medium-chain Acyl CoA dehydrogenase [Enzymatic activity/mass] in Fibroblast"
        value = 2.0
        try:
            concentration = int(value)
            m = Measurements.percent(code=loinc_code,
                                     label=loinc_label,
                                     concentration=concentration)
        except Exception:
            pass
        assert isinstance(m, Measurement202)
        ontology_class = m.assay
        assert ontology_class.id == loinc_code
        assert ontology_class.label == loinc_label
        test_value = m.value.value.value
        assert test_value == 2.0
        unit = m.value.value.unit
        assert unit.id == "UCUM:%"
        assert unit.label == "percent"




 