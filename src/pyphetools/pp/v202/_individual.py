import typing

import phenopackets as pp202

from google.protobuf.message import Message


from ._base import TimeElement
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_pb_message_scalar


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
        self._alt_ids = [] if alternate_ids is None else list(alternate_ids)
        self._time_at_last_encounter = time_at_last_encounter

    @property
    def id(self) -> typing.Optional[str]:
        return self._id

    @property
    def alternate_ids(self) -> typing.MutableSequence[str]:
        return self._alt_ids

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

    def to_message(self) -> Message:
        i = pp202.Individual(
            id=self._id,
        )

        if len(self._alt_ids) != 0:
            i.alternate_ids.extend(self._alt_ids)

        if self._time_at_last_encounter is not None:
            i.time_at_last_encounter.CopyFrom(self._time_at_last_encounter.to_message())

        return i

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Individual

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Individual):
            return Individual(
                id=msg.id,
                alternate_ids=msg.alternate_ids,
                time_at_last_encounter=extract_pb_message_scalar('time_at_last_encounter', TimeElement, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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
