import pytest

from pyphetools.creation import AgeIsoFormater


class TestAgeIsoFormater:

    @pytest.mark.parametrize(
        'year, month, day, iso',
        [
            ( 2, 3,  5, "P2Y3M5D"),
            ( 29, 5,  25, "P29Y5M25D"),
            ( 99,1,24,"P99Y1M24D"),
        ]
    )
    def test_ymd(
        self,
        year: int, 
        month: int, 
        day: int,
        iso:str,
    ):
        iso_age = AgeIsoFormater.to_string(y=year, m=month, d=day)
        assert iso == iso_age

    @pytest.mark.parametrize(
        'month, iso',
        [
            ( 5, "P5M"),
            ( 0.5,"P15D"),
            (0.8, "P24D"),
            (11, "P11M"),
            (12, "P1Y"),
            (16, "P1Y4M"),
            ("n.a.", "NOT_PROVIDED"),
            (None, "NOT_PROVIDED"),
            (float("nan"), "NOT_PROVIDED"),
            (0, "P0D")
        ]
    )
    def test_numerical_month(
        self,
        month: float, 
        iso: str
    ):
        iso_age = AgeIsoFormater.from_numerical_month(month=month)
        assert iso == iso_age

    





