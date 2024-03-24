import pytest

from pyphetools.pp import Timestamp


class TestTimestamp:

    @pytest.mark.parametrize(
        'left, right, expected',
        [
            ('1970-01-01T00:00:01Z', '1970-01-01T00:00:01Z', True),
            ('1970-01-01T10:00:00Z', '1970-01-01T06:00:00-04:00', True),  # EDT is 4 hrs behind UTC
        ]
    )
    def test_time_zones(
            self,
            left: str, right: str, expected: bool):
        left = Timestamp.from_str(left)
        right = Timestamp.from_str(right)
        assert (left == right) == expected

    @pytest.mark.parametrize(
        'dt, seconds, nanos',
        [
            ('1970-01-01T00:00:00Z', 0, 0),
            ('1970-01-01T04:00:00+04:00', 0, 0),
        ]
    )
    def test_from_str(
            self,
            dt: str, seconds: int, nanos: int,
    ):
        ts = Timestamp.from_str(dt)

        assert ts.seconds == seconds
        assert ts.nanos == nanos

    @pytest.mark.parametrize(
        'seconds, nanos, expected',
        [
            (0, 0, '1970-01-01T00:00:00Z'),
            (10, 0, '1970-01-01T00:00:10Z'),
            (-10, 0, '1969-12-31T23:59:50Z'),
            (-10, 0, '1969-12-31T23:59:50Z'),
        ]
    )
    def test_as_str(
            self,
            seconds: int, nanos: int, expected: str):
        ts = Timestamp(seconds, nanos)
        assert ts.as_str() == expected

    def test_nanos(self):
        ts = Timestamp(10, 10_000)
        assert ts.seconds == 10
        assert ts.nanos == 10_000

        assert ts.as_str() == '1970-01-01T00:00:10Z'
        assert ts.as_str(fmt='%Y-%m-%dT%H:%M:%S.%fZ') == '1970-01-01T00:00:10.000010Z'
