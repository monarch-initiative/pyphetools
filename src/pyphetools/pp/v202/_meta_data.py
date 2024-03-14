import typing

from .._api import MessageMixin


class MetaData(MessageMixin):

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        return MetaData()

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return ()

    def __eq__(self, other):
        return isinstance(other, MetaData)

    def __repr__(self):
        return f'MetaData()'
