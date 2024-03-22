import typing

import phenopackets as pp202
from google.protobuf.message import Message

from .._api import MessageMixin


class GeneDescriptor(MessageMixin):

    def __init__(
            self,
            value_id: str,
            symbol: str,
            description: typing.Optional[str] = None,
            alternate_ids: typing.Optional[typing.Iterable[str]] = None,
            xrefs: typing.Optional[typing.Iterable[str]] = None,
            alternate_symbols: typing.Optional[typing.Iterable[str]] = None,
    ):
        self._value_id = value_id
        self._symbol = symbol
        self._description = description
        self._alternate_ids = [] if alternate_ids is None else list(alternate_ids)
        self._xrefs = [] if xrefs is None else list(xrefs)
        self._alternate_symbols = [] if alternate_symbols is None else list(alternate_symbols)

    @property
    def value_id(self) -> str:
        return self._value_id

    @value_id.setter
    def value_id(self, value: str):
        self._value_id = value

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._symbol = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @description.deleter
    def description(self):
        self._description = None

    @property
    def alternate_ids(self) -> typing.MutableSequence[str]:
        return self._alternate_ids

    @property
    def xrefs(self) -> typing.MutableSequence[str]:
        return self._xrefs

    @property
    def alternate_symbols(self) -> typing.MutableSequence[str]:
        return self._alternate_symbols

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'value_id', 'symbol', 'description', 'alternate_ids', 'xrefs', 'alternate_symbols',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'value_id', 'symbol',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return GeneDescriptor(
                value_id=values['value_id'],
                symbol=values['symbol'],
                description=values.get('description', None),
                alternate_ids=values.get('alternate_ids', None),
                xrefs=values.get('xrefs', None),
                alternate_symbols=values.get('alternate_symbols', None),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        gene_descriptor = pp202.GeneDescriptor(value_id=self._value_id, symbol=self._symbol)

        if self._description is not None:
            gene_descriptor.description = self._description

        gene_descriptor.alternate_ids.extend(self._alternate_ids)
        gene_descriptor.xrefs.extend(self._xrefs)
        gene_descriptor.alternate_symbols.extend(self._alternate_symbols)

        return gene_descriptor

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.GeneDescriptor

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return GeneDescriptor(
                value_id=msg.value_id,
                symbol=msg.symbol,
                description=None if msg.description == '' else msg.description,
                alternate_ids=msg.alternate_ids,
                xrefs=msg.xrefs,
                alternate_symbols=msg.alternate_symbols,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, GeneDescriptor) \
            and self._value_id == other._value_id \
            and self._symbol == other._symbol \
            and self._description == other._description \
            and self._alternate_ids == other._alternate_ids \
            and self._xrefs == other._xrefs \
            and self._alternate_symbols == other._alternate_symbols

    def __repr__(self):
        return f'GeneDescriptor(' \
               f'value_id={self._value_id}, ' \
               f'symbol={self._symbol}, ' \
               f'description={self._description}, ' \
               f'alternate_ids={self._alternate_ids}, ' \
               f'xrefs={self._xrefs}, ' \
               f'alternate_symbols={self._alternate_symbols})'
