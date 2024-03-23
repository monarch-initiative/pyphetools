import typing

import phenopackets as pp202
from google.protobuf.message import Message

from .._api import MessageMixin
from ._base import OntologyClass, Procedure, TimeElement
from ..parse import extract_message_scalar, extract_message_sequence, extract_oneof_scalar
from ..parse import extract_pb_message_scalar, extract_pb_message_seq, extract_pb_oneof_scalar


class ReferenceRange(MessageMixin):

    def __init__(
            self,
            unit: OntologyClass,
            low: float,
            high: float,
    ):
        self._unit = unit
        self._low = low
        self._high = high

    @property
    def unit(self) -> OntologyClass:
        return self._unit

    @unit.setter
    def unit(self, value: OntologyClass):
        self._unit = value

    @property
    def low(self) -> float:
        return self._low

    @low.setter
    def low(self, value: float):
        self._low = value

    @property
    def high(self) -> float:
        return self._high

    @high.setter
    def high(self, value: float):
        self._high = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'unit', 'low', 'high'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'unit', 'low', 'high'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return ReferenceRange(
                unit=extract_message_scalar('unit', OntologyClass, values),
                low=values['low'],
                high=values['high'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.ReferenceRange(
            unit=self._unit.to_message(),
            low=self._low,
            high=self._high,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.ReferenceRange

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return ReferenceRange(
                unit=extract_pb_message_scalar('unit', OntologyClass, msg),
                low=msg.low,
                high=msg.high,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, ReferenceRange) \
            and self._unit == other._unit \
            and self._low == other._low \
            and self._high == other._high

    def __repr__(self):
        return f'ReferenceRange(unit={self._unit}, low={self._low}, high={self._high})'


class Quantity(MessageMixin):

    def __init__(
            self,
            unit: OntologyClass,
            value: float,
            reference_range: typing.Optional[ReferenceRange] = None,
    ):
        self._unit = unit
        self._value = value
        self._reference_range = reference_range

    @property
    def unit(self) -> OntologyClass:
        return self._unit

    @unit.setter
    def unit(self, value: OntologyClass):
        self._unit = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def reference_range(self) -> typing.Optional[ReferenceRange]:
        return self._reference_range

    @reference_range.setter
    def reference_range(self, value: ReferenceRange):
        self._reference_range = value

    @reference_range.deleter
    def reference_range(self):
        self._reference_range = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'unit', 'value', 'reference_range'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'unit', 'value'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Quantity(
                unit=extract_message_scalar('unit', OntologyClass, values),
                value=values['value'],
                reference_range=extract_message_scalar('reference_range', ReferenceRange, values),
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Quantity

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Quantity(
                unit=extract_pb_message_scalar('unit', OntologyClass, msg),
                value=msg.value,
                reference_range=extract_pb_message_scalar('reference_range', ReferenceRange, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def to_message(self) -> Message:
        quantity = pp202.Quantity(unit=self._unit.to_message(), value=self._value)

        if self._reference_range is not None:
            quantity.reference_range.CopyFrom(self._reference_range.to_message())

        return quantity

    def __eq__(self, other):
        return isinstance(other, Quantity) \
            and self._unit == other._unit \
            and self._value == other._value \
            and self._reference_range == other._reference_range

    def __repr__(self):
        return f'Quantity(unit={self._unit}, value={self._value}, reference_range={self._reference_range})'


class TypedQuantity(MessageMixin):

    def __init__(
            self,
            type: OntologyClass,
            quantity: Quantity,
    ):
        self._type = type
        self._quantity = quantity

    @property
    def type(self) -> OntologyClass:
        return self._type

    @type.setter
    def type(self, value: OntologyClass):
        self._type = value

    @property
    def quantity(self) -> Quantity:
        return self._quantity

    @quantity.setter
    def quantity(self, value: Quantity):
        self._quantity = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'type', 'quantity'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'type', 'quantity'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return TypedQuantity(
                type=extract_message_scalar('type', OntologyClass, values),
                quantity=extract_message_scalar('quantity', Quantity, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.TypedQuantity(
            type=self._type.to_message(),
            quantity=self._quantity.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.TypedQuantity

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return TypedQuantity(
                type=extract_pb_message_scalar('type', OntologyClass, msg),
                quantity=extract_pb_message_scalar('quantity', Quantity, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, TypedQuantity) \
            and self._type == other._type \
            and self._quantity == other._quantity

    def __repr__(self):
        return f'TypedQuantity(type={self._type}, quantity={self._quantity})'


class ComplexValue(MessageMixin):

    def __init__(
            self,
            typed_quantities: typing.Iterable[TypedQuantity],
    ):
        self._typed_quantities = list(typed_quantities)
        if len(self._typed_quantities) < 0:
            raise ValueError(f'At least 1 typed quantity must be present!')

    @property
    def typed_quantities(self) -> typing.MutableSequence[TypedQuantity]:
        return self._typed_quantities

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'typed_quantities',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'typed_quantities',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return ComplexValue(
                typed_quantities=extract_message_sequence('typed_quantities', TypedQuantity, values),
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.ComplexValue

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return ComplexValue(
                typed_quantities=extract_pb_message_seq('typed_quantities', TypedQuantity, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def to_message(self) -> Message:
        cv = pp202.ComplexValue()
        cv.typed_quantities.extend(m.to_message() for m in self._typed_quantities)
        return cv

    def __eq__(self, other):
        return isinstance(other, ComplexValue) \
            and self._typed_quantities == other._typed_quantities

    def __repr__(self):
        return f'ComplexValue(typed_quantities={self._typed_quantities})'


class Value(MessageMixin):
    _ONEOF_VALUE = {'quantity': Quantity, 'ontology_class': OntologyClass}

    def __init__(
            self,
            value: typing.Union[Quantity, OntologyClass],
    ):
        self._value = value

    @property
    def value(self) -> typing.Union[Quantity, OntologyClass]:
        return self._value

    @property
    def quantity(self) -> typing.Optional[Quantity]:
        return self._value if isinstance(self._value, Quantity) else None

    @quantity.setter
    def quantity(self, value: Quantity):
        self._value = value

    @property
    def ontology_class(self) -> typing.Optional[OntologyClass]:
        return self._value if isinstance(self._value, OntologyClass) else None

    @ontology_class.setter
    def ontology_class(self, value: OntologyClass):
        self._value = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'quantity', 'ontology_class'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(field in values for field in cls._ONEOF_VALUE):
            return Value(
                value=extract_oneof_scalar(cls._ONEOF_VALUE, values),
            )
        else:
            raise ValueError(f'Missing one of required fields: `quantity|ontology_class`: {values}')

    def to_message(self) -> Message:
        v = pp202.Value()

        if isinstance(self._value, Quantity):
            v.quantity.CopyFrom(self._value.to_message())
        elif isinstance(self._value, OntologyClass):
            v.ontology_class.CopyFrom(self._value.to_message())
        else:
            raise ValueError('Bug')

        return v

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Value

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Value(
                value=extract_pb_oneof_scalar('value', cls._ONEOF_VALUE, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Value) and self._value == other._value

    def __repr__(self):
        return f'Value(value={self._value})'


class Measurement(MessageMixin):
    _ONEOF_MEASUREMENT_VALUE = {'value': Value, 'complex_value': ComplexValue}

    def __init__(
            self,
            assay: OntologyClass,
            measurement_value: typing.Union[Value, ComplexValue],
            description: typing.Optional[str] = None,
            time_observed: typing.Optional[TimeElement] = None,
            procedure: typing.Optional[Procedure] = None,
    ):
        self._assay = assay
        self._measurement_value = measurement_value
        self._description = description
        self._time_observed = time_observed
        self._procedure = procedure

    @property
    def assay(self) -> OntologyClass:
        return self._assay

    @assay.setter
    def assay(self, value: OntologyClass):
        self._assay = value

    @property
    def measurement_value(self) -> typing.Union[Value, ComplexValue]:
        return self._measurement_value

    @property
    def value(self) -> typing.Optional[Value]:
        return self._measurement_value if isinstance(self._measurement_value, Value) else None

    @property
    def complex_value(self) -> typing.Optional[ComplexValue]:
        return self._measurement_value if isinstance(self._measurement_value, ComplexValue) else None

    @property
    def description(self) -> typing.Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @description.deleter
    def description(self):
        self._description = None

    @property
    def time_observed(self) -> typing.Optional[TimeElement]:
        return self._time_observed

    @time_observed.setter
    def time_observed(self, value: TimeElement):
        self._time_observed = value

    @time_observed.deleter
    def time_observed(self):
        self._time_observed = None

    @property
    def procedure(self) -> typing.Optional[Procedure]:
        return self._procedure

    @procedure.setter
    def procedure(self, value: Procedure):
        self._procedure = value

    @procedure.deleter
    def procedure(self):
        self._procedure = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'assay', 'value', 'complex_value', 'description', 'time_observed', 'procedure'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if 'assay' in values and any(field in values for field in cls._ONEOF_MEASUREMENT_VALUE):
            return Measurement(
                assay=extract_message_scalar('assay', OntologyClass, values),
                measurement_value=extract_oneof_scalar(cls._ONEOF_MEASUREMENT_VALUE, values),
                description=values.get('description', None),
                time_observed=extract_message_scalar('time_observed', TimeElement, values),
                procedure=extract_message_scalar('procedure', Procedure, values),
            )
        else:
            raise ValueError(f'Missing one of required fields: `assay, value|complex_value` {values}')

    def to_message(self) -> Message:
        m = pp202.Measurement(
            assay=self._assay.to_message(),
        )

        if isinstance(self._measurement_value, Value):
            m.value.CopyFrom(self._measurement_value.to_message())
        elif isinstance(self._measurement_value, ComplexValue):
            m.complex_value.CopyFrom(self._measurement_value.to_message())
        else:
            raise ValueError('Bug')

        if self._description is not None:
            m.description = self._description

        if self._time_observed is not None:
            m.time_observed.CopyFrom(self._time_observed.to_message())

        if self._procedure is not None:
            m.procedure.CopyFrom(self._procedure.to_message())

        return m

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Measurement

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Measurement(
                assay=extract_pb_message_scalar('assay', OntologyClass, msg),
                measurement_value=extract_pb_oneof_scalar(
                    'measurement_value',
                    cls._ONEOF_MEASUREMENT_VALUE,
                    msg),
                description=None if msg.description == '' else msg.description,
                time_observed=extract_pb_message_scalar('time_observed', TimeElement, msg),
                procedure=extract_pb_message_scalar('procedure', Procedure, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Measurement) \
            and self._assay == other._assay \
            and self._measurement_value == other._measurement_value \
            and self._description == other._description \
            and self._time_observed == other._time_observed \
            and self._procedure == other._procedure

    def __repr__(self):
        return f'Measurement(' \
               f'assay={self._assay}, ' \
               f'measurement_value={self._measurement_value}, ' \
               f'description={self._description}, ' \
               f'time_observed={self._time_observed}, ' \
               f'procedure={self._procedure})'
