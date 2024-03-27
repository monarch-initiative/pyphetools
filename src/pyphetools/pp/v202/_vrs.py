import typing

import phenopackets as pp202
from google.protobuf.message import Message

from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq
from ..parse import extract_oneof_scalar, extract_pb_oneof_scalar


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


class IndefiniteRange(MessageMixin):

    def __init__(
            self,
            value: int,
            comparator: str,
    ):
        self._value = value
        self._comparator = comparator

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value

    @property
    def comparator(self) -> str:
        return self._comparator

    @comparator.setter
    def comparator(self, value: str):
        self._comparator = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'value', 'comparator'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'value', 'comparator'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return IndefiniteRange(
                value=values['value'],
                comparator=values['comparator'],
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.IndefiniteRange

    def to_message(self) -> Message:
        return pp202.IndefiniteRange(
            value=self._value,
            comparator=self._comparator,
        )

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return IndefiniteRange(
                value=msg.value,
                comparator=msg.comparator,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, IndefiniteRange) \
            and self._value == other._value \
            and self._comparator == other._comparator

    def __repr__(self):
        return f'IndefiniteRange(value={self._value}, comparator={self._comparator})'


class DefiniteRange(MessageMixin):

    def __init__(
            self,
            min: int,
            max: int,
    ):
        self._min = min
        self._max = max

    @property
    def min(self) -> int:
        return self._min

    @min.setter
    def min(self, value: int):
        self._min = value

    @property
    def max(self) -> int:
        return self._max

    @max.setter
    def max(self, value: int):
        self._max = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'min', 'max'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'min', 'max'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return DefiniteRange(
                min=values['min'],
                max=values['max'],
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.DefiniteRange

    def to_message(self) -> Message:
        return pp202.DefiniteRange(min=self._min, max=self._max)

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return DefiniteRange(
                min=msg.min,
                max=msg.max,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, DefiniteRange) \
            and self._min == other._min \
            and self._max == other._max

    def __repr__(self):
        return f'DefiniteRange(min={self._min}, max={self._max})'


class SimpleInterval(MessageMixin):

    def __init__(
            self,
            start: int,
            end: int,
    ):
        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        return self._start

    @start.setter
    def start(self, value: int):
        self._start = value

    @property
    def end(self) -> int:
        return self._end

    @end.setter
    def end(self, value: int):
        self._end = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'start', 'end'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'start', 'end'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return SimpleInterval(
                start=values['start'],
                end=values['end'],
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.SimpleInterval

    def to_message(self) -> Message:
        return pp202.SimpleInterval(start=self._start, end=self._end)

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return SimpleInterval(
                start=msg.start,
                end=msg.end,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, SimpleInterval) \
            and self._start == other._start \
            and self._end == other._end

    def __repr__(self):
        return f'SimpleInterval(start={self._start}, end={self._end})'


class SequenceInterval:

    def __init__(
            self,
            start: typing.Union[Number, IndefiniteRange, DefiniteRange],
            end: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._start = start
        self._end = end


class SequenceLocation:
    # TODO:

    def __init__(
            self,
            sequence_id: str,
            interval: typing.Union[SequenceInterval, SimpleInterval],
    ):
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


class DerivedSequenceExpression(MessageMixin):

    def __init__(
            self,
            location: SequenceLocation,
            reverse_complement: bool,
    ):
        self._location = location
        self._reverse_complement = reverse_complement

    @property
    def location(self) -> SequenceLocation:
        return self._location

    @location.setter
    def location(self, value: SequenceLocation):
        self._location = value

    @property
    def reverse_complement(self) -> bool:
        return self._reverse_complement

    @reverse_complement.setter
    def reverse_complement(self, value: bool):
        self._reverse_complement = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'location', 'reverse_complement'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'location', 'reverse_complement'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return DerivedSequenceExpression(
                location=extract_message_scalar('location', SequenceLocation, values),
                reverse_complement=values['reverse_complement'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.DerivedSequenceExpression(
            location=self._location.to_message(),
            reverse_complement=self._reverse_complement,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.DerivedSequenceExpression

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return DerivedSequenceExpression(
                location=extract_pb_message_scalar('location', SequenceLocation, msg),
                reverse_complement=msg.reverse_complement,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, DerivedSequenceExpression) \
            and self._location == other._location \
            and self._reverse_complement == other._reverse_complement

    def __repr__(self):
        return f'DerivedSequenceExpression(location={self._location}, reverse_complement={self._reverse_complement})'


class RepeatedSequenceExpression(MessageMixin):
    _ONEOF_SEQ_EXPRESSION = {
        'literal_sequence_expression': LiteralSequenceExpression,
        'derived_sequence_expression': DerivedSequenceExpression,
    }
    _ONEOF_COUNT = {
        'number': Number, 'indefinite_range': IndefiniteRange, 'definite_range': DefiniteRange,
    }

    def __init__(
            self,
            seq_expr: typing.Union[LiteralSequenceExpression, DerivedSequenceExpression],
            count: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._seq_expr = seq_expr
        self._count = count

    @property
    def seq_expr(self) -> typing.Union[LiteralSequenceExpression, DerivedSequenceExpression]:
        return self._seq_expr

    @property
    def literal_sequence_expression(self) -> typing.Optional[LiteralSequenceExpression]:
        return self._seq_expr if isinstance(self._seq_expr, LiteralSequenceExpression) else None

    @literal_sequence_expression.setter
    def literal_sequence_expression(self, value: LiteralSequenceExpression):
        self._seq_expr = value

    @property
    def derived_sequence_expression(self) -> typing.Optional[DerivedSequenceExpression]:
        return self._seq_expr if isinstance(self._seq_expr, DerivedSequenceExpression) else None

    @derived_sequence_expression.setter
    def derived_sequence_expression(self, value: DerivedSequenceExpression):
        self._seq_expr = value

    @property
    def count(self) -> typing.Union[Number, IndefiniteRange, DefiniteRange]:
        return self._count

    @property
    def number(self) -> typing.Optional[Number]:
        return self._count if isinstance(self._count, Number) else None

    @number.setter
    def number(self, value: Number):
        self._count = value

    @property
    def indefinite_range(self) -> typing.Optional[IndefiniteRange]:
        return self._count if isinstance(self._count, IndefiniteRange) else None

    @indefinite_range.setter
    def indefinite_range(self, value: IndefiniteRange):
        self._count = value

    @property
    def definite_range(self):
        return self._count if isinstance(self._count, DefiniteRange) else None

    @definite_range.setter
    def definite_range(self, value: DefiniteRange):
        self._count = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return (
            'literal_sequence_expression', 'derived_sequence_expression',
            'number', 'indefinite_range', 'definite_range',
        )

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(f in values for f in cls._ONEOF_SEQ_EXPRESSION) \
                and any(f in values for f in cls._ONEOF_COUNT):
            return RepeatedSequenceExpression(
                seq_expr=extract_oneof_scalar(cls._ONEOF_SEQ_EXPRESSION, values),
                count=extract_oneof_scalar(cls._ONEOF_COUNT, values),
            )
        else:
            raise ValueError(
                'Missing one of required fields: ' 
                '`literal_sequence_expression|derived_sequence_expression` or '
                f'`number|indefinite_range|definite_range`: {values}'
                )

    def to_message(self) -> Message:
        e = pp202.RepeatedSequenceExpression()

        # `seq_expr`
        if isinstance(self._seq_expr, LiteralSequenceExpression):
            e.literal_sequence_expression.CopyFrom(self._seq_expr.to_message())
        elif isinstance(self._seq_expr, DerivedSequenceExpression):
            e.derived_sequence_expression.CopyFrom(self._seq_expr.to_message())
        else:
            raise ValueError('Bug')

        # `count`
        if isinstance(self._count, Number):
            e.number.CopyFrom(self._count.to_message())
        elif isinstance(self._count, IndefiniteRange):
            e.indefinite_range.CopyFrom(self._count.to_message())
        elif isinstance(self._count, DefiniteRange):
            e.definite_range.CopyFrom(self._count.to_message())
        else:
            raise ValueError('Bug')

        return e

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.RepeatedSequenceExpression

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return RepeatedSequenceExpression(
                seq_expr=extract_pb_oneof_scalar('seq_expr', cls._ONEOF_SEQ_EXPRESSION, msg),
                count=extract_pb_oneof_scalar('count', cls._ONEOF_COUNT, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, RepeatedSequenceExpression) \
            and self._seq_expr == other._seq_expr \
            and self._count == other._count

    def __repr__(self):
        return f'RepeatedSequenceExpression(seq_expr={self._seq_expr}, count={self._count})'


class CytobandInterval(MessageMixin):

    def __init__(
            self,
            start: str,
            end: str,
    ):
        self._start = start
        self._end = end

    @property
    def start(self) -> str:
        return self._start

    @start.setter
    def start(self, value: str):
        self._start = value

    @property
    def end(self) -> str:
        return self._end

    @end.setter
    def end(self, value: str):
        self._end = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'start', 'end'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'start', 'end'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return CytobandInterval(
                start=values['start'],
                end=values['end'],
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.CytobandInterval

    def to_message(self) -> Message:
        return pp202.CytobandInterval(start=self._start, end=self._end)

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return CytobandInterval(
                start=msg.start,
                end=msg.end,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, CytobandInterval) \
            and self._start == other._start \
            and self._end == other._end

    def __repr__(self):
        return f'CytobandInterval(start={self._start}, end={self._end})'


class ChromosomeLocation(MessageMixin):

    def __init__(
            self,
            species_id: str,
            chr: str,
            interval: CytobandInterval,
    ):
        self._species_id = species_id
        self._chr = chr
        self._interval = interval

    @property
    def species_id(self) -> str:
        return self._species_id

    @species_id.setter
    def species_id(self, value: str):
        self._species_id = value

    @property
    def chr(self) -> str:
        return self._chr

    @chr.setter
    def chr(self, value: str):
        self._chr = value

    @property
    def interval(self) -> CytobandInterval:
        return self._interval

    @interval.setter
    def interval(self, value: CytobandInterval):
        self._interval = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'species_id', 'chr', 'interval'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'species_id', 'chr', 'interval'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return ChromosomeLocation(
                species_id=values['species_id'],
                chr=values['chr'],
                interval=extract_message_scalar('interval', CytobandInterval, values),
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.ChromosomeLocation

    def to_message(self) -> Message:
        return pp202.ChromosomeLocation(
            species_id=self._species_id,
            chr=self._chr,
            interval=self._interval.to_message(),
        )

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return ChromosomeLocation(
                species_id=msg.species_id,
                chr=msg.chr,
                interval=extract_pb_message_scalar('interval', CytobandInterval, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, ChromosomeLocation) \
            and self._species_id == other._species_id \
            and self._chr == other._chr \
            and self._interval == other._interval

    def __repr__(self):
        return f'ChromosomeLocation(species_id={self._species_id}, chr={self._chr}, interval={self._interval})'


class Allele:
    # TODO:

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
    # TODO:

    class Member:
        def __init__(
                self,
                value: typing.Union[Allele, str],
        ):
            self._value = value

    def __init__(
            self,
            members: typing.Iterable[Member],
    ):
        self._members = list(members)


class CopyNumber:
    # TODO:

    def __init__(
            self,
            subject: typing.Union[
                Allele, Haplotype, Gene,
                LiteralSequenceExpression, DerivedSequenceExpression, RepeatedSequenceExpression,
                str,
            ],
            copies: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._subject = subject
        self._copies = copies


class VariationSet:
    # TODO:

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
            members: typing.Iterable[Member],
    ):
        self._members = list(members)


class Variation:
    # TODO:

    def __init__(
            self,
            variation: typing.Union[Allele, Haplotype, CopyNumber, Text, VariationSet],
    ):
        self._variation = variation
