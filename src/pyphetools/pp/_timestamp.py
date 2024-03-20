import math
import typing
from datetime import datetime

from google.protobuf.message import Message
from google.protobuf.timestamp_pb2 import Timestamp as PbTimestamp

from .parse import ToProtobuf, FromProtobuf


class Timestamp(ToProtobuf, FromProtobuf):
    """
    A Timestamp represents a point in time independent of any time zone or local
    calendar, encoded as a count of seconds and fractions of seconds at
    nanosecond resolution. The count is relative to an epoch at UTC midnight on
    January 1, 1970, in the proleptic Gregorian calendar which extends the
    Gregorian calendar backwards to year one.

    Consult the `Phenopacket Schema <https://phenopacket-schema.readthedocs.io/en/latest/timestamp.html>`_ documentation
    for more information.

    **Examples**

    Here we show how to create a `Timestamp` from various inputs.

    >>> from pyphetools.pp import Timestamp

    Let's create a timestamp from a date time string:

    >>> ts = Timestamp.from_str('2021-05-14T10:35:00Z')
    >>> ts.seconds, ts.nanos  # doctest: +SKIP
    (1621002900, 0)

    We can create Timestamp from a datetime object:

    >>> from datetime import datetime, date, time
    >>> d = date(2021, 5, 14)
    >>> t = time(10, 35, 00)
    >>> dt = datetime.combine(d, t)
    >>> ts = Timestamp.from_datetime(dt)
    >>> ts.seconds, ts.nanos  # doctest: +SKIP
    (1621002900, 0)

    and we get the same timestamp as above.

    Last, we can create a timestamp directly from seconds and nanoseconds:

    >>> ts = Timestamp(1_621_002_900, 1)
    >>> ts.seconds, ts.nanos  # doctest: +SKIP
    (1621002900, 1)
    """

    def __init__(
            self,
            seconds: int,
            nanos: int,
    ):
        self._seconds = seconds
        self._nanos = nanos

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

    def as_str(self, fmt: str = '%Y-%m-%dT%H:%M:%SZ') -> str:
        """
        Convert timestamp into a date time string.

        **Example**

        >>> from pyphetools.pp import Timestamp
        >>> ts = Timestamp(123_456, 111_222)
        >>> ts.as_str()  # doctest: +SKIP
        '1970-01-02T05:17:36Z'

        We can use different formatting:

        >>> ts.as_str('%Y-%m-%dT%H:%M:%S.%fZ')  # doctest: +SKIP
        '1970-01-02T05:17:36.111222Z'
        """

        dt = datetime.fromtimestamp(self._seconds + (self._nanos / 1_000_000))
        return dt.strftime(fmt)

    @staticmethod
    def from_str(val: str, fmt: str = '%Y-%m-%dT%H:%M:%SZ'):
        """
        Create `Timestamp` from a date time string.

        :param val: the date time `str`.
        :param fmt: the date time format string.
        """
        return Timestamp.from_datetime(datetime.strptime(val, fmt))

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
