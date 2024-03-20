import math
import typing
from datetime import datetime, timezone

from google.protobuf.message import Message
from google.protobuf.timestamp_pb2 import Timestamp as PbTimestamp

from .parse import ToProtobuf, FromProtobuf


class Timestamp(ToProtobuf, FromProtobuf):
    """
    This `Timestamp` implementation is functionally equivalent to protobuf's timestamp.

    Per protobuf API documentation, *A Timestamp represents a point in time
    independent of any time zone or local calendar, encoded as a count of seconds
    and fractions of seconds at nanosecond resolution.
    The count is relative to an epoch at UTC midnight on January 1, 1970,
    in the proleptic Gregorian calendar which extends the Gregorian calendar
    backwards to year one.*

    Consult the `Phenopacket Schema <https://phenopacket-schema.readthedocs.io/en/latest/timestamp.html>`_ documentation
    for more information.

    **Examples**

    Here we show how to create a `Timestamp` from various inputs.

    >>> from pyphetools.pp import Timestamp

    Let's create a timestamp from a date time string:

    >>> ts = Timestamp.from_str('1970-01-01T00:00:30Z')
    >>> ts.seconds, ts.nanos
    (30, 0)

    Note, we indicate that the timestamp is in UTC by adding `Z` suffix.

    We can also create a timestamp from a local time.
    Let's create the same `Timestamp` but now in Eastern Daylight Time (EDT)
    which is 4 hours behind UTC:

    >>> ts_local = Timestamp.from_str('1969-12-31T20:00:30-04:00')
    >>> assert ts_local == ts

    We can also create timestamp from a datetime object:

    >>> from datetime import datetime, date, time, timezone
    >>> d = date(1970, 1, 1)
    >>> t = time(0, 0, 30)
    >>> dt = datetime.combine(d, t, tzinfo=timezone.utc)
    >>> ts_dt = Timestamp.from_datetime(dt)
    >>> assert ts_dt == ts

    Last, we can create timestamp directly from seconds and nanoseconds:

    >>> ts_raw = Timestamp(30, 0)
    >>> assert ts_raw == ts

    and we can convert the timestamp to a UTC date time string:

    >>> ts_raw.as_str()
    '1970-01-01T00:00:30Z'
    """

    def __init__(
            self,
            seconds: int,
            nanos: int,
    ):
        # Seconds can be positive or negative,
        # The negative seconds represent the timestamps prior the UNIX epoch.
        self._seconds = seconds
        self._nanos = nanos  # TODO: check that nanos is a positive `int`

    @property
    def seconds(self) -> int:
        return self._seconds

    @seconds.setter
    def seconds(self, value: int):
        self._seconds = value

    @property
    def nanos(self) -> int:
        return self._nanos

    @nanos.setter
    def nanos(self, value: int):
        self._nanos = value

    def as_datetime(self) -> datetime:
        """
        Convert timestamp into Python's datetime object.

        The datetime is always in UTC.

        **Example**

        >>> from pyphetools.pp import Timestamp
        >>> ts = Timestamp(10, 500)
        >>> dt = ts.as_datetime()

        Now we can access the datetime components:

        >>> dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        (1970, 1, 1, 0, 0, 10)

        including the time zone:

        >>> dt.tzname()
        'UTC'
        """
        return datetime.fromtimestamp(self._seconds + (self._nanos / 10 ** 9), tz=timezone.utc)

    def as_str(self, fmt: str = '%Y-%m-%dT%H:%M:%SZ') -> str:
        """
        Convert timestamp into a date time string.

        **Example**

        >>> from pyphetools.pp import Timestamp
        >>> ts = Timestamp(0, 500_000)
        >>> ts.as_str()
        '1970-01-01T00:00:00Z'

        We can use different formatting:

        >>> ts.as_str('%Y-%m-%dT%H:%M:%S.%f%Z')
        '1970-01-01T00:00:00.000500UTC'
        """
        return self.as_datetime().strftime(fmt)

    @staticmethod
    def from_str(val: str, fmt: str = '%Y-%m-%dT%H:%M:%S%z'):
        """
        Create `Timestamp` from a date time string.

        :param val: the date time `str`.
        :param fmt: the date time format string.
        """
        dt = datetime.strptime(val, fmt)
        return Timestamp.from_datetime(dt)

    @staticmethod
    def from_datetime(dt: datetime):
        fractional, integral = math.modf(dt.timestamp())
        return Timestamp(seconds=int(integral), nanos=int(fractional * 1_000_000))

    def to_message(self) -> Message:
        return PbTimestamp(seconds=self._seconds, nanos=self._nanos)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return PbTimestamp

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, PbTimestamp):
            return Timestamp(
                seconds=msg.seconds,
                nanos=msg.nanos,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Timestamp) \
            and self._seconds == other._seconds \
            and self._nanos == other._nanos

    def __repr__(self):
        return f'Timestamp(seconds={self._seconds}, nanos={self._nanos})'
