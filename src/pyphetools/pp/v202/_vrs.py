import typing

import phenopackets as pp202
from google.protobuf.message import Message

from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class Gene(MessageMixin):

    def __init__(
            self,
            gene_id: str,
    ):
        self._gene_id = gene_id

    @property
    def gene_id(self) -> str:
        return self._gene_id

    @gene_id.setter
    def gene_id(self, value: str):
        self._gene_id = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'gene_id',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'gene_id',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Gene(
                gene_id=values['gene_id'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Gene(gene_id=self._gene_id)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Gene

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Gene(
                gene_id=msg.gene_id,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Gene) and self._gene_id == other._gene_id

    def __repr__(self):
        return f'Gene(gene_id={self._gene_id})'


class Text(MessageMixin):

    def __init__(
            self,
            definition: str,
    ):
        self._definition = definition

    @property
    def definition(self) -> str:
        return self._definition

    @definition.setter
    def definition(self, value: str):
        self._definition = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'definition',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'definition',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Text(
                definition=values['definition'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Text(definition=self._definition)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Text

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Text(
                definition=msg.definition,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Text) and self._definition == other._definition

    def __repr__(self):
        return f'Text(definition={self._definition})'


class Number(MessageMixin):

    def __init__(
            self,
            value: int,
    ):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'value',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'value',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Number(
                value=values['value'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Number(value=self._value)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Number

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Number(
                value=msg.value,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Number) and self._value == other._value

    def __repr__(self):
        return f'Number(value={self._value})'


class IndefiniteRange:

    def __init__(
            self,
            value: int,
            comparator: str,
    ):
        self._value = value
        self._comparator = comparator


class DefiniteRange:

    def __init__(
            self,
            min: int,
            max: int,
    ):
        self._min = min
        self._max = max


class SimpleInterval:

    def __init__(
            self,
            start: int,
            end: int,
    ):
        self._start = start
        self._end = end


class SequenceInterval:

    def __init__(
            self,
            start: typing.Union[Number, IndefiniteRange, DefiniteRange],
            end: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._start = start
        self._end = end


class SequenceLocation:

    def __init__(
            self,
            _id: str,
            sequence_id: str,
            interval: typing.Union[SequenceInterval, SimpleInterval],
    ):
        self._id = _id
        self._sequence_id = sequence_id
        self._interval = interval


class SequenceState(MessageMixin):

    def __init__(
            self,
            sequence: str,
    ):
        self._sequence = sequence

    @property
    def sequence(self) -> str:
        return self._sequence

    @sequence.setter
    def sequence(self, value: str):
        self._sequence = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'sequence',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'sequence',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return SequenceState(
                sequence=values['sequence'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.SequenceState(sequence=self._sequence)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.SequenceState

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return SequenceState(
                sequence=msg.sequence,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, SequenceState) and self._sequence == other._sequence

    def __repr__(self):
        return f'SequenceState(sequence={self._sequence})'
    

class LiteralSequenceExpression(MessageMixin):

    def __init__(
            self,
            sequence: str,
    ):
        self._sequence = sequence

    @property
    def sequence(self) -> str:
        return self._sequence

    @sequence.setter
    def sequence(self, value: str):
        self._sequence = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'sequence',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'sequence',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return LiteralSequenceExpression(
                sequence=values['sequence'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.LiteralSequenceExpression(sequence=self._sequence)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.LiteralSequenceExpression

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return LiteralSequenceExpression(
                sequence=msg.sequence,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, LiteralSequenceExpression) and self._sequence == other._sequence

    def __repr__(self):
        return f'LiteralSequenceExpression(sequence={self._sequence})'


class DerivedSequenceExpression:

    def __init__(
            self,
            location: SequenceLocation,
            reverse_complement: bool,
    ):
        self._location = location
        self._reverse_complement = reverse_complement


class RepeatedSequenceExpression:

    def __init__(
            self,
            seq_expr: typing.Union[LiteralSequenceExpression, DerivedSequenceExpression],
            count: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._seq_expr = seq_expr
        self._count = count,


class CytobandInterval:

    def __init__(
            self,
            start: str,
            end: str,
    ):
        self._start = start
        self._end = end


class ChromosomeLocation:

    def __init__(
            self,
            _id: str,
            species_id: str,
            chr: str,
            interval: CytobandInterval,
    ):
        self._id = _id
        self._species_id = species_id
        self._chr = chr
        self._interval = interval


class Allele:

    def __init__(
            self,
            _id: str,
            location: typing.Union[str, ChromosomeLocation, SequenceLocation],
            state: typing.Union[
                SequenceState, LiteralSequenceExpression,
                DerivedSequenceExpression, RepeatedSequenceExpression,
            ],
    ):
        self._id = _id
        self._location = location
        self._state = state


class Haplotype:
    class Member:
        def __init__(
                self,
                value: typing.Union[Allele, str],
        ):
            self._value = value

    def __init__(
            self,
            _id: str,
            members: typing.Iterable[Member],
    ):
        self._id = _id
        self._members = list(members)


class CopyNumber:

    def __init__(
            self,
            _id: str,
            subject: typing.Union[
                Allele, Haplotype, Gene,
                LiteralSequenceExpression, DerivedSequenceExpression, RepeatedSequenceExpression,
                str,
            ],
            copies: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._id = _id
        self._subject = subject
        self._copies = copies


class VariationSet:
    class Member:
        """

        **IMPORTANT**: `value` can also be an instance of :class:`VariationSet`!
        """

        def __init__(
                self,
                value: typing.Union[str, Allele, Haplotype, CopyNumber, Text],
        ):
            self._value = value
            if isinstance(value, VariationSet):
                pass

    def __init__(
            self,
            _id: str,
            members: typing.Iterable[Member],
    ):
        self._id = _id
        self._members = list(members)


class Variation:

    def __init__(
            self,
            variation: typing.Union[Allele, Haplotype, CopyNumber, Text, VariationSet],
    ):
        self._variation = variation
