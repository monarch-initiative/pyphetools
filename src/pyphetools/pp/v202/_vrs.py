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
            value: typing.Union[int, str],
    ):
        if isinstance(value, str):
            self._value = int(value)
        else:
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


class SequenceInterval(MessageMixin):
    """
    `SequenceInterval` is a complicated case which is
    """
    _ONE_OF_START_FIELDS = ('start_number', 'start_indefinite_range', 'start_definite_range')
    _ONE_OF_END_FIELDS = ('end_number', 'end_indefinite_range', 'end_definite_range')

    # `SequenceInterval` is a degenerate case, because `start` and `end` oneof fields consist of the same value types.
    # Protobuf solves this by appending the type to field name.
    # For instance, it stores `start` in one of `startNumber`, `startIndefiniteRange`, `startDefiniteRange`
    # depending on the type, and `end` as `endNumber`, `endIndefiniteRange`, `endDefiniteRange`
    # for the other field.,
    #
    # We will do the same for the purpose of (de)serialization.

    def __init__(
            self,
            start: typing.Union[Number, IndefiniteRange, DefiniteRange],
            end: typing.Union[Number, IndefiniteRange, DefiniteRange],
    ):
        self._start = start
        self._end = end

    @property
    def start(self) -> typing.Union[Number, IndefiniteRange, DefiniteRange]:
        return self._start

    @property
    def start_number(self) -> typing.Optional[Number]:
        return self._start if isinstance(self._start, Number) else None

    @start_number.setter
    def start_number(self, value: Number):
        self._start = value

    @property
    def start_indefinite_range(self) -> typing.Optional[IndefiniteRange]:
        return self._start if isinstance(self._start, IndefiniteRange) else None

    @start_indefinite_range.setter
    def start_indefinite_range(self, value: IndefiniteRange):
        self._start = value

    @property
    def start_definite_range(self) -> typing.Optional[DefiniteRange]:
        return self._start if isinstance(self._start, DefiniteRange) else None

    @start_definite_range.setter
    def start_definite_range(self, value: DefiniteRange):
        self._start = value

    @property
    def end(self) -> typing.Union[Number, IndefiniteRange, DefiniteRange]:
        return self._end

    @property
    def end_number(self) -> typing.Optional[Number]:
        return self._end if isinstance(self._end, Number) else None

    @end_number.setter
    def end_number(self, value: Number):
        self._end = value

    @property
    def end_indefinite_range(self) -> typing.Optional[IndefiniteRange]:
        return self._end if isinstance(self._end, IndefiniteRange) else None

    @end_indefinite_range.setter
    def end_indefinite_range(self, value: IndefiniteRange):
        self._end = value

    @property
    def end_definite_range(self) -> typing.Optional[DefiniteRange]:
        return self._end if isinstance(self._end, DefiniteRange) else None

    @end_definite_range.setter
    def end_definite_range(self, value: DefiniteRange):
        self._end = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    def to_dict(self, out: typing.MutableMapping[str, typing.Any]):
        # A rather verbose implementation.

        # start
        start = {}
        self._start.to_dict(start)
        if isinstance(self._start, Number):
            name = 'start_number'
        elif isinstance(self._start, IndefiniteRange):
            name = 'start_indefinite_range'
        elif isinstance(self._start, DefiniteRange):
            name = 'start_definite_range'
        else:
            raise ValueError('Bug')
        out[name] = start

        # end
        end = {}
        self._end.to_dict(end)
        if isinstance(self._end, Number):
            name = 'end_number'
        elif isinstance(self._end, IndefiniteRange):
            name = 'end_indefinite_range'
        elif isinstance(self._end, DefiniteRange):
            name = 'end_definite_range'
        else:
            raise ValueError('Bug')
        out[name] = end

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(f in values for f in cls._ONE_OF_START_FIELDS) \
                and any(f in values for f in cls._ONE_OF_END_FIELDS):
            if 'start_number' in values:
                start = extract_message_scalar('start_number', Number, values)
            elif 'start_indefinite_range' in values:
                start = extract_message_scalar('start_indefinite_range', IndefiniteRange, values)
            elif 'start_definite_range' in values:
                start = extract_message_scalar('start_definite_range', DefiniteRange, values)
            else:
                raise ValueError('Bug')

            if 'end_number' in values:
                end = extract_message_scalar('end_number', Number, values)
            elif 'end_indefinite_range' in values:
                end = extract_message_scalar('end_indefinite_range', IndefiniteRange, values)
            elif 'end_definite_range' in values:
                end = extract_message_scalar('end_definite_range', DefiniteRange, values)
            else:
                raise ValueError('Bug')

            return SequenceInterval(
                start=start,
                end=end,
            )
        else:
            raise ValueError(f'Missing one of required fields: `assay, value|complex_value` {values}')

    def to_message(self) -> Message:
        si = pp202.SequenceInterval()

        # TODO:
        # I am not sure about the attribute where we should be setting this.
        # Both for `start` and `end`
        if isinstance(self._start, Number):
            si.start.CopyFrom(self._start.to_message())
        elif isinstance(self._start, IndefiniteRange):
            si.start.CopyFrom(self._start.to_message())
        elif isinstance(self._start, DefiniteRange):
            si.start.CopyFrom(self._start.to_message())
        else:
            raise ValueError('Bug')

        if isinstance(self._end, Number):
            si.end.CopyFrom(self._end.to_message())
        elif isinstance(self._end, IndefiniteRange):
            si.end.CopyFrom(self._end.to_message())
        elif isinstance(self._end, DefiniteRange):
            si.end.CopyFrom(self._end.to_message())
        else:
            raise ValueError('Bug')

        return si

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.SequenceInterval

    @classmethod
    def from_message(cls, msg: Message):
        print(msg)
        raise NotImplementedError()  # TODO: implement

    def __eq__(self, other):
        return isinstance(other, SequenceInterval) \
            and self._start == other._start \
            and self._end == other._end

    def __repr__(self):
        return f'SequenceInterval(' \
               f'start={self._start}, ' \
               f'end={self._end})'


class SequenceLocation(MessageMixin):
    _ONEOF_INTERVAL_VALUE = {'sequence_interval': SequenceInterval, 'simple_interval': SimpleInterval}

    def __init__(
            self,
            sequence_id: str,
            interval: typing.Union[SequenceInterval, SimpleInterval],
    ):
        self._sequence_id = sequence_id
        self._interval = interval

    @property
    def sequence_id(self) -> str:
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, value: str):
        self._sequence_id = value

    @property
    def interval(self) -> typing.Union[SequenceInterval, SimpleInterval]:
        return self._interval

    @property
    def sequence_interval(self):
        return self._interval if isinstance(self._interval, SequenceInterval) else None

    @sequence_interval.setter
    def sequence_interval(self, value: SequenceInterval):
        self._interval = value

    @property
    def simple_interval(self):
        return self._interval if isinstance(self._interval, SimpleInterval) else None

    @simple_interval.setter
    def simple_interval(self, value: SimpleInterval):
        self._interval = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'sequence_id', 'sequence_interval', 'simple_interval'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if 'sequence_id' in values and any(f in values for f in cls._ONEOF_INTERVAL_VALUE):
            return SequenceLocation(
                sequence_id=values['sequence_id'],
                interval=extract_oneof_scalar(cls._ONEOF_INTERVAL_VALUE, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.SequenceLocation(
            sequence_id=self._sequence_id,
            interval=self._interval.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.SequenceLocation

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return SequenceLocation(
                sequence_id=msg.sequence_id,
                interval=extract_pb_oneof_scalar('interval', cls._ONEOF_INTERVAL_VALUE, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, SequenceLocation) \
            and self._sequence_id == other._sequence_id \
            and self._interval == other._interval

    def __repr__(self):
        return f'SequenceLocation(sequence_id={self._sequence_id}, interval={self._interval})'


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
            reverse_complement: bool = False,
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
        return 'location',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return DerivedSequenceExpression(
                location=extract_message_scalar('location', SequenceLocation, values),
                reverse_complement=values['reverse_complement'] if 'reverse_complement' in values else False,
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


class Allele(MessageMixin):
    _ONEOF_LOCATION = {
        'curie': str,
        'chromosome_location': ChromosomeLocation,
        'sequence_location': SequenceLocation,
    }
    _ONEOF_STATE = {
        'sequence_state': SequenceState,
        'literal_sequence_expression': LiteralSequenceExpression,
        'derived_sequence_expression': DerivedSequenceExpression,
        'repeated_sequence_expression': RepeatedSequenceExpression,
    }

    def __init__(
            self,
            location: typing.Union[str, ChromosomeLocation, SequenceLocation],
            state: typing.Union[
                SequenceState, LiteralSequenceExpression,
                DerivedSequenceExpression, RepeatedSequenceExpression,
            ],
    ):
        self._location = location
        self._state = state

    @property
    def location(self) -> typing.Union[str, ChromosomeLocation, SequenceLocation]:
        return self._location

    @property
    def curie(self) -> typing.Optional[str]:
        return self._location if isinstance(self._location, str) else None

    @curie.setter
    def curie(self, value: str):
        self._location = value

    @property
    def chromosome_location(self) -> typing.Optional[ChromosomeLocation]:
        return self._location if isinstance(self._location, ChromosomeLocation) else None

    @chromosome_location.setter
    def chromosome_location(self, value: ChromosomeLocation):
        self._location = value

    @property
    def sequence_location(self) -> typing.Optional[SequenceLocation]:
        return self._location if isinstance(self._location, SequenceLocation) else None

    @sequence_location.setter
    def sequence_location(self, value: SequenceLocation):
        self._location = value

    @property
    def state(self) -> typing.Union[
        SequenceState, LiteralSequenceExpression,
        DerivedSequenceExpression, RepeatedSequenceExpression,
    ]:
        return self._state

    @property
    def sequence_state(self) -> typing.Optional[SequenceState]:
        return self._state if isinstance(self._state, SequenceState) else None

    @sequence_state.setter
    def sequence_state(self, value: SequenceState):
        self._state = value

    @property
    def literal_sequence_expression(self) -> typing.Optional[LiteralSequenceExpression]:
        return self._state if isinstance(self._state, LiteralSequenceExpression) else None

    @literal_sequence_expression.setter
    def literal_sequence_expression(self, value: LiteralSequenceExpression):
        self._state = value

    @property
    def derived_sequence_expression(self) -> typing.Optional[DerivedSequenceExpression]:
        return self._state if isinstance(self._state, DerivedSequenceExpression) else None

    @derived_sequence_expression.setter
    def derived_sequence_expression(self, value: DerivedSequenceExpression):
        self._state = value

    @property
    def repeated_sequence_expression(self) -> typing.Optional[RepeatedSequenceExpression]:
        return self._state if isinstance(self._state, RepeatedSequenceExpression) else None

    @repeated_sequence_expression.setter
    def repeated_sequence_expression(self, value: RepeatedSequenceExpression):
        self._state = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return (
            'curie', 'chromosome_location', 'sequence_location',
            'sequence_state', 'literal_sequence_expression',
            'derived_sequence_expression', 'repeated_sequence_expression',
        )

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(f in values for f in cls._ONEOF_LOCATION) and any(f in values for f in cls._ONEOF_STATE):
            # We must extract the location in a special way because `not isinstance(curie, Deserializable)`.
            if 'curie' in values:
                location = values['curie']
            else:
                location = extract_oneof_scalar(cls._ONEOF_LOCATION, values)

            return Allele(
                location=location,
                state=extract_oneof_scalar(cls._ONEOF_STATE, values),
            )
        else:
            raise ValueError(
                'Missing one of required fields: '
                '`curie|chromosome_location|,sequence_location` '
                '`sequence_state|literal_sequence_expression|derived_sequence_expression|repeated_sequence_expression`'
                f' {values}')

    def to_message(self) -> Message:
        a = pp202.Allele(
            state=self._state.to_message(),
        )

        if isinstance(self._location, str):
            a.curie = self._location
        elif isinstance(self._location, ChromosomeLocation):
            a.chromosome_location.CopyFrom(self._location.to_message())
        elif isinstance(self._location, SequenceLocation):
            a.sequence_location.CopyFrom(self._location.to_message())
        else:
            raise ValueError('Bug')

        return a

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Allele

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            location = msg.WhichOneof('location')
            if location == 'curie':
                loc = msg.curie
            else:
                loc = extract_pb_oneof_scalar('location', cls._ONEOF_LOCATION, msg)
            return Allele(
                location=loc,
                state=extract_pb_oneof_scalar('state', cls._ONEOF_STATE, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Allele) \
            and self._location == other._location \
            and self._state == other._state

    def __repr__(self):
        return f'Allele(' \
               f'location={self._location}, ' \
               f'state={self._state})'


class Haplotype(MessageMixin):
    class Member(MessageMixin):

        def __init__(
                self,
                value: typing.Union[Allele, str],
        ):
            self._value = value

        @property
        def value(self) -> typing.Union[Allele, str]:
            return self._value

        @property
        def allele(self) -> typing.Optional[Allele]:
            return self._value if isinstance(self._value, Allele) else None

        @allele.setter
        def allele(self, value: Allele):
            self._value = value

        @property
        def curie(self) -> typing.Optional[str]:
            return self._value if isinstance(self._value, str) else None

        @curie.setter
        def curie(self, value: str):
            self._value = value

        @staticmethod
        def field_names() -> typing.Iterable[str]:
            return 'allele', 'curie',

        @classmethod
        def required_fields(cls) -> typing.Sequence[str]:
            raise NotImplementedError('Should not be called!')

        @classmethod
        def from_dict(cls, values: typing.Mapping[str, typing.Any]):
            if any(f in values for f in ('allele', 'curie')):
                # We must extract the value in a special way because `not isinstance(curie, Deserializable)`.
                if 'curie' in values:
                    value = values['curie']
                else:
                    value = extract_message_scalar('allele', Allele, values)

                return Haplotype.Member(
                    value=value,
                )
            else:
                raise ValueError(f'Missing one of required fields: `curie|allele` {values}')

        def to_message(self) -> Message:
            hm = pp202.Haplotype.Member()

            if isinstance(self._value, str):
                hm.curie = self._value
            elif isinstance(self._value, Allele):
                hm.allele.CopyFrom(self._value.to_message())
            else:
                raise ValueError('Bug')

            return hm

        @classmethod
        def message_type(cls) -> typing.Type[Message]:
            return pp202.Haplotype.Member

        @classmethod
        def from_message(cls, msg: Message):
            if isinstance(msg, cls.message_type()):
                which = msg.WhichOneof('value')
                if which == 'curie':
                    value = msg.curie
                else:
                    value = extract_pb_message_scalar('allele', Allele, msg)
                return pp202.Haplotype.Member(
                    value=value,
                )
            else:
                cls.complain_about_incompatible_msg_type(msg)

        def __eq__(self, other):
            return isinstance(other, Haplotype.Member) \
                and self._value == other._value

        def __repr__(self):
            return f'Haplotype.Member(value={self._value})'

    def __init__(
            self,
            members: typing.Iterable[Member],
    ):
        self._members = list(members)

    @property
    def members(self) -> typing.MutableSequence[Member]:
        return self._members

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'members',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'members',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Haplotype(
                members=extract_message_sequence('members', Haplotype.Member, values)
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Haplotype(members=(m.to_message() for m in self._members))

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Haplotype

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Haplotype(
                members=extract_pb_message_seq('members', Haplotype.Member, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Haplotype) \
            and self._members == other._members

    def __repr__(self):
        return f'Haplotype(members={self._members})'


class CopyNumber(MessageMixin):
    _ONEOF_SUBJECT = {
        'allele': Allele,
        'haplotype': Haplotype,
        'gene': Gene,
        'literal_sequence_expression': LiteralSequenceExpression,
        'derived_sequence_expression': DerivedSequenceExpression,
        'repeated_sequence_expression': RepeatedSequenceExpression,
        'curie': str,
    }
    _ONEOF_COPIES = {
        'number': Number,
        'indefinite_range': DefiniteRange,
        'definite_range': DefiniteRange,
    }

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

    @property
    def subject(self) -> typing.Union[
        Allele, Haplotype, Gene,
        LiteralSequenceExpression, DerivedSequenceExpression, RepeatedSequenceExpression,
        str,
    ]:
        return self._subject

    @property
    def allele(self) -> typing.Optional[Allele]:
        return self._subject if isinstance(self._subject, Allele) else None

    @allele.setter
    def allele(self, value: Allele):
        self._subject = value

    @property
    def haplotype(self) -> typing.Optional[Haplotype]:
        return self._subject if isinstance(self._subject, Haplotype) else None

    @haplotype.setter
    def haplotype(self, value: Haplotype):
        self._subject = value

    @property
    def gene(self) -> typing.Optional[Gene]:
        return self._subject if isinstance(self._subject, Gene) else None

    @gene.setter
    def gene(self, value: Gene):
        self._subject = value

    @property
    def literal_sequence_expression(self) -> typing.Optional[LiteralSequenceExpression]:
        return self._subject if isinstance(self._subject, LiteralSequenceExpression) else None

    @literal_sequence_expression.setter
    def literal_sequence_expression(self, value: LiteralSequenceExpression):
        self._subject = value

    @property
    def derived_sequence_expression(self) -> typing.Optional[DerivedSequenceExpression]:
        return self._subject if isinstance(self._subject, DerivedSequenceExpression) else None

    @derived_sequence_expression.setter
    def derived_sequence_expression(self, value: DerivedSequenceExpression):
        self._subject = value

    @property
    def repeated_sequence_expression(self) -> typing.Optional[RepeatedSequenceExpression]:
        return self._subject if isinstance(self._subject, RepeatedSequenceExpression) else None

    @repeated_sequence_expression.setter
    def repeated_sequence_expression(self, value: RepeatedSequenceExpression):
        self._subject = value

    @property
    def curie(self) -> typing.Optional[str]:
        return self._subject if isinstance(self._subject, str) else None

    @curie.setter
    def curie(self, value: str):
        self._subject = value

    @property
    def copies(self) -> typing.Union[Number, IndefiniteRange, DefiniteRange]:
        return self._copies

    @property
    def number(self) -> typing.Optional[Number]:
        return self._copies if isinstance(self._copies, Number) else None

    @number.setter
    def number(self, value: Number):
        self._copies = value

    @property
    def indefinite_range(self) -> typing.Optional[IndefiniteRange]:
        return self._copies if isinstance(self._copies, IndefiniteRange) else None

    @indefinite_range.setter
    def indefinite_range(self, value: IndefiniteRange):
        self._copies = value

    @property
    def definite_range(self) -> typing.Optional[DefiniteRange]:
        return self._copies if isinstance(self._copies, DefiniteRange) else None

    @definite_range.setter
    def definite_range(self, value: DefiniteRange):
        self._copies = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return (
            'allele', 'haplotype', 'gene',
            'literal_sequence_expression', 'derived_sequence_expression', 'repeated_sequence_expression', 'curie',
            'number', 'indefinite_range', 'definite_range',
        )

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(f in values for f in cls._ONEOF_SUBJECT) and any(f in values for f in cls._ONEOF_COPIES):
            # We must extract the subject in a special way because `not isinstance(curie, Deserializable)`.
            if 'curie' in values:
                subject = values['curie']
            else:
                subject = extract_oneof_scalar(cls._ONEOF_SUBJECT, values)

            return CopyNumber(
                subject=subject,
                copies=extract_oneof_scalar(cls._ONEOF_COPIES, values),
            )
        else:
            raise ValueError(
                'Missing one of required fields: '
                f'`{"|".join(cls._ONEOF_SUBJECT)}` ',
                f'`{"|".join(cls._ONEOF_COPIES)}` in ',
                f'{values}')

    def to_message(self) -> Message:
        cn = pp202.CopyNumber()

        # subject
        if isinstance(self._subject, Allele):
            cn.allele = self._subject.to_message()
        elif isinstance(self._subject, Haplotype):
            cn.haplotype.CopyFrom(self._subject.to_message())
        elif isinstance(self._subject, Gene):
            cn.gene.CopyFrom(self._subject.to_message())
        elif isinstance(self._subject, LiteralSequenceExpression):
            cn.literal_sequence_expression.CopyFrom(self._subject.to_message())
        elif isinstance(self._subject, DerivedSequenceExpression):
            cn.derived_sequence_expression.CopyFrom(self._subject.to_message())
        elif isinstance(self._subject, RepeatedSequenceExpression):
            cn.repeated_sequence_expression.CopyFrom(self._subject.to_message())
        elif isinstance(self._subject, str):
            cn.curie = self._subject
        else:
            raise ValueError('Bug')

        # copies
        if isinstance(self._copies, Number):
            cn.number = self._copies.to_message()
        elif isinstance(self._copies, IndefiniteRange):
            cn.indefinite_range.CopyFrom(self._copies.to_message())
        elif isinstance(self._copies, DefiniteRange):
            cn.definite_range.CopyFrom(self._copies.to_message())
        else:
            raise ValueError('Bug')

        return cn

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.CopyNumber

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            subject = msg.WhichOneof('subject')
            if subject == 'curie':
                sub = msg.curie
            else:
                sub = extract_pb_oneof_scalar('subject', cls._ONEOF_SUBJECT, msg)
            return CopyNumber(
                subject=sub,
                copies=extract_pb_oneof_scalar('copies', cls._ONEOF_COPIES, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, CopyNumber) \
            and self._subject == other._subject \
            and self._copies == other._copies

    def __repr__(self):
        return f'CopyNumber(' \
               f'subject={self._subject}, ' \
               f'copies={self._copies})'


class VariationSet(MessageMixin):
    class Member(MessageMixin):
        _ONEOF_VALUE = {
            # 'curie': str,
            'allele': Allele, 'haplotype': Haplotype,
            'copy_number': CopyNumber, 'text': Text,
            # 'variation_set': VariationSet,
        }
        """

        **IMPORTANT**: `value` can also be an instance of :class:`VariationSet`!
        """

        def __init__(
                self,
                value: typing.Union[str, Allele, Haplotype, CopyNumber, Text],
        ):
            self._value = value

        @property
        def value(self) -> typing.Union[str, Allele, Haplotype, CopyNumber, Text]:
            return self._value

        @property
        def curie(self) -> typing.Optional[str]:
            return self._value if isinstance(self._value, str) else None

        @curie.setter
        def curie(self, value: str):
            self._value = value

        @property
        def allele(self) -> typing.Optional[Allele]:
            return self._value if isinstance(self._value, Allele) else None

        @allele.setter
        def allele(self, value: Allele):
            self._value = value

        @property
        def haplotype(self) -> typing.Optional[Haplotype]:
            return self._value if isinstance(self._value, Haplotype) else None

        @haplotype.setter
        def haplotype(self, value: Haplotype):
            self._value = value

        @property
        def copy_number(self) -> typing.Optional[CopyNumber]:
            return self._value if isinstance(self._value, CopyNumber) else None

        @copy_number.setter
        def copy_number(self, value: CopyNumber):
            self._value = value

        @property
        def text(self) -> typing.Optional[Text]:
            return self._value if isinstance(self._value, Text) else None

        @text.setter
        def text(self, value: Text):
            self._value = value

        @property
        def variation_set(self):
            """
            Get :class:`VariationSet` if present or `None` if `value` contains a different type.
            """
            return self._value if isinstance(self._value, VariationSet) else None

        @variation_set.setter
        def variation_set(self, value):
            """
            Set the :class:`VariationSet` as the value. Setting value is a no-op if `value`
            is not an instance of :class:`VariationSet`.

            Note, there is no type annotation on this method, but it should
            """
            if isinstance(value, VariationSet):
                self._value = value

        @staticmethod
        def field_names() -> typing.Iterable[str]:
            return 'curie', 'allele', 'haplotype', 'copy_number', 'text', 'variation_set',

        @classmethod
        def required_fields(cls) -> typing.Sequence[str]:
            raise NotImplementedError('Should not be called!')

        @classmethod
        def from_dict(cls, values: typing.Mapping[str, typing.Any]):
            if 'curie' in values or any(f in values for f in cls._ONEOF_VALUE) or 'variation_set' in values:
                if 'curie' in values:
                    return VariationSet.Member(value=values['curie'])
                elif 'variation_set' in values:
                    # Disabling the false positive warning below - we cannot add VariationSet into the __init__
                    # but it is an acceptable value.
                    # noinspection PyTypeChecker
                    return VariationSet.Member(value=extract_message_scalar('variation_set', VariationSet, values))
                else:
                    return VariationSet.Member(value=extract_oneof_scalar(cls._ONEOF_VALUE, values))
            else:
                raise ValueError(
                    'Missing one of required fields: `curie|allele|haplotype|copy_number|text|variation_set` in ',
                    f'{values}')

        def to_message(self) -> Message:
            m = pp202.VariationSet.Member()

            if isinstance(self._value, str):
                m.curie = self._value
            elif isinstance(self._value, Allele):
                m.allele = self._value.to_message()
            elif isinstance(self._value, Haplotype):
                m.haplotype.CopyFrom(self._value.to_message())
            elif isinstance(self._value, CopyNumber):
                m.copy_number.CopyFrom(self._value.to_message())
            elif isinstance(self._value, Text):
                m.text.CopyFrom(self._value.to_message())
            elif isinstance(self._value, VariationSet):
                m.variation_set.CopyFrom(self._value.to_message())
            else:
                raise ValueError('Bug')

            return m

        @classmethod
        def message_type(cls) -> typing.Type[Message]:
            return pp202.VariationSet.Member

        @classmethod
        def from_message(cls, msg: Message):
            if isinstance(msg, cls.message_type()):
                which = msg.WhichOneof('value')
                if which == 'curie':
                    return VariationSet.Member(value=msg.curie)
                elif which == 'variation_set':
                    # Same as in `from_dict`, the warning is false positive.
                    # noinspection PyTypeChecker
                    return VariationSet.Member(value=extract_pb_message_scalar('variation_set', VariationSet, msg))
                else:
                    return VariationSet.Member(
                        value=extract_pb_oneof_scalar('value', cls._ONEOF_VALUE, msg),
                    )
            else:
                cls.complain_about_incompatible_msg_type(msg)

        def __eq__(self, other):
            return isinstance(other, VariationSet.Member) \
                and self._value == other._value

        def __repr__(self):
            return f'VariationSet.Member(value={self._value})'

    def __init__(
            self,
            members: typing.Iterable[Member],
    ):
        self._members = list(members)

    @property
    def members(self) -> typing.MutableSequence[Member]:
        return self._members

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'members',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'members',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return VariationSet(
                members=extract_message_sequence('members', VariationSet.Member, values)
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.VariationSet(members=(m.to_message() for m in self._members))

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.VariationSet

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return VariationSet(
                members=extract_pb_message_seq('members', VariationSet.Member, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, VariationSet) \
            and self._members == other._members

    def __repr__(self):
        return f'VariationSet(members={self._members})'


class Variation(MessageMixin):
    _ONEOF_VARIATION = {
        'allele': Allele, 'haplotype': Haplotype, 'copy_number': CopyNumber,
        'text': Text, 'variation_set': VariationSet,
    }

    def __init__(
            self,
            variation: typing.Union[Allele, Haplotype, CopyNumber, Text, VariationSet],
    ):
        self._variation = variation

    @property
    def variation(self) -> typing.Union[Allele, Haplotype, CopyNumber, Text, VariationSet]:
        return self._variation

    @property
    def allele(self) -> typing.Optional[Allele]:
        return self._variation if isinstance(self._variation, Allele) else None

    @allele.setter
    def allele(self, value: Allele):
        self._variation = value

    @property
    def haplotype(self) -> typing.Optional[Haplotype]:
        return self._variation if isinstance(self._variation, Haplotype) else None

    @haplotype.setter
    def haplotype(self, value: Haplotype):
        self._variation = value

    @property
    def copy_number(self) -> typing.Optional[CopyNumber]:
        return self._variation if isinstance(self._variation, CopyNumber) else None

    @copy_number.setter
    def copy_number(self, value: CopyNumber):
        self._variation = value

    @property
    def text(self) -> typing.Optional[Text]:
        return self._variation if isinstance(self._variation, Text) else None

    @text.setter
    def text(self, value: Text):
        self._variation = value

    @property
    def variation_set(self) -> typing.Optional[VariationSet]:
        return self._variation if isinstance(self._variation, VariationSet) else None

    @variation_set.setter
    def variation_set(self, value: VariationSet):
        self._variation = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'allele', 'haplotype', 'copy_number', 'text', 'variation_set',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(f in values for f in cls._ONEOF_VARIATION):
            return Variation(
                variation=extract_oneof_scalar(cls._ONEOF_VARIATION, values),
            )
        else:
            raise ValueError(
                'Missing one of required fields: '
                f'`{"|".join(cls._ONEOF_VARIATION)}` in ',
                f'{values}')

    def to_message(self) -> Message:
        v = pp202.Variation()

        if isinstance(self._variation, Allele):
            v.allele = self._variation.to_message()
        elif isinstance(self._variation, Haplotype):
            v.haplotype.CopyFrom(self._variation.to_message())
        elif isinstance(self._variation, CopyNumber):
            v.copy_number.CopyFrom(self._variation.to_message())
        elif isinstance(self._variation, Text):
            v.text.CopyFrom(self._variation.to_message())
        elif isinstance(self._variation, VariationSet):
            v.variation_set.CopyFrom(self._variation.to_message())
        else:
            raise ValueError('Bug')

        return v

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Variation

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Variation(
                variation=extract_pb_oneof_scalar('variation', cls._ONEOF_VARIATION, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Variation) \
            and self._variation == other._variation

    def __repr__(self):
        return f'Variation(variation={self._variation})'
