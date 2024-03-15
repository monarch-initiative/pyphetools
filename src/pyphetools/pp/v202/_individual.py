import typing

from ._base import TimeElement
from .._api import MessageMixin
from ..parse import extract_message_scalar


class Individual(MessageMixin):

    def __init__(
            self,
            id: str,
            alternate_ids: typing.Optional[typing.Iterable[str]] = None,
            # date_of_birth
            time_at_last_encounter: typing.Optional[TimeElement] = None,
    ):
        # TODO: validate
        self._id = id
        self._alt_ids = None if alternate_ids is None else tuple(alternate_ids)
        self._time_at_last_encounter = time_at_last_encounter

    @property
    def id(self) -> typing.Optional[str]:
        return self._id

    @property
    def alternate_ids(self) -> typing.Optional[typing.Sequence[str]]:
        return self._alt_ids

    @alternate_ids.setter
    def alternate_ids(self, value: typing.Optional[typing.Sequence[str]]):
        self._alt_ids = value

    @property
    def time_at_last_encounter(self) -> typing.Optional[TimeElement]:
        return self._time_at_last_encounter

    @time_at_last_encounter.setter
    def time_at_last_encounter(self, value: typing.Optional[TimeElement]):
        self._time_at_last_encounter = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'alternate_ids', 'time_at_last_encounter',

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        return Individual(
            id=values['id'],
            alternate_ids=MessageMixin._extract_optional_field('alternate_ids', values),
            time_at_last_encounter=extract_message_scalar('time_at_last_encounter', TimeElement, values),
        )

    def __eq__(self, other):
        return isinstance(other, Individual) \
            and self._id == other._id \
            and self._alt_ids == other._alt_ids \
            and self._time_at_last_encounter == other._time_at_last_encounter

    def __repr__(self):
        return f'Individual(id={self._id},' \
               f' alternate_ids={self._alt_ids},' \
               f' time_at_last_encounter={self._time_at_last_encounter},' \
               ')'
