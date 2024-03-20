import pytest

from ._base import *


class TestBase:
    """
    Test base elements of the Phenopacket Schema v2.0.2.
    """

    def test_time_element__no_args(self):
        with pytest.raises(ValueError) as ve:
            TimeElement()

        assert ve.value.args[0] == 'Time element must be provided with exactly 1 argument but 0 arguments were provided!'

    def test_time_element__more_args(self):
        with pytest.raises(ValueError) as ve:
            TimeElement(
                gestational_age=GestationalAge(weeks=3),
                age=Age(iso8601duration='P33Y'),
            )

        assert ve.value.args[0] == 'Time element must be provided with exactly 1 argument but 2 arguments were provided!'
