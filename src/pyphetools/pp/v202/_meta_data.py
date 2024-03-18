import typing

import phenopackets as pp202
from google.protobuf.message import Message

from .._api import MessageMixin


class MetaData(MessageMixin):
    # TODO: this entire class must be implemented!

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        return MetaData()

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return ()

    def to_message(self) -> Message:
        return pp202.MetaData()

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.MetaData

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.MetaData):
            return MetaData(
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, MetaData)

    def __repr__(self):
        return f'MetaData()'
