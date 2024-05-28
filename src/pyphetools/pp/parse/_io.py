import abc
import enum
import io
import typing


class Serializable(metaclass=abc.ABCMeta):
    """
    `Serializable` is a mixin class for data classes composed of a hierarchy of primitive types, such as `bool`, `int`,
    `float`, or `str`, or other `Serializable` objects.

    `Serializable` knows how to convert the data into a hierarchy composed of primitive types
    or Python compound types such as `list` and `dict`. The hierarchy is an intermediate step before serializing
    into a data format such as JSON, YAML or others using a :class:Serializer`.

    The mixin requirements include a single method: :func:`field_names` and the other functionality then comes for free.
    """

    _PRIMITIVES = {
        bool, int, float, str,
    }

    @staticmethod
    @abc.abstractmethod
    def field_names() -> typing.Iterable[str]:
        """
        Get an iterable with the data class field names.
        """
        pass

    def to_dict(self,
                out: typing.MutableMapping[str, typing.Any]):
        """
        Write itself into a dictionary composed of primitive or Python compound types.
        """
        for name in self.field_names():
            field = getattr(self, name)
            Serializable._put_field_to_mapping(name, field, out)

    @staticmethod
    def _put_field_to_mapping(
            name: str,
            field: typing.Optional[typing.Any],
            out: typing.MutableMapping[str, typing.Any],
    ):
        if field is None:
            pass
        elif type(field) in Serializable._PRIMITIVES:
            out[name] = field
        elif isinstance(field, typing.Sequence):
            seq = []
            for subfield in field:
                Serializable._put_field_to_sequence(subfield, seq)
            out[name] = seq
        elif isinstance(field, typing.Mapping):
            val = {}
            for k, v in field.items():
                Serializable._put_field_to_mapping(k, v, val)
            out[name] = val
        elif isinstance(field, Serializable):
            val = {}
            field.to_dict(val)
            out[name] = val
        elif isinstance(field, enum.Enum):
            out[name] = field.name
        elif hasattr(field, 'seconds') and hasattr(field, 'nanos') and hasattr(field, 'as_str') and callable(field.as_str):
            # This quacks *exactly* as a Timestamp!
            out[name] = field.as_str()
        else:
            raise ValueError(f'Unexpected field {field}')

    @staticmethod
    def _put_field_to_sequence(
            field: typing.Optional[typing.Any],
            out: typing.MutableSequence[typing.Any],
    ):
        if field is None:
            pass
        elif type(field) in Serializable._PRIMITIVES:
            out.append(field)
        elif isinstance(field, Serializable):
            val = {}
            for field_name in field.field_names():
                sub = getattr(field, field_name)
                Serializable._put_field_to_mapping(field_name, sub, val)
            out.append(val)
        elif isinstance(field, typing.Mapping):
            val = {}
            for k, v in field.items():
                Serializable._put_field_to_mapping(k, v, val)
            out.append(val)
        elif isinstance(field, enum.Enum):
            out.append(field.name)
        elif hasattr(field, 'seconds') and hasattr(field, 'nanos') and hasattr(field, 'as_str') and callable(field.as_str):
            # This quack *exactly* as a Timestamp!
            out.append(field.as_str())
        else:
            # We should not have to process a sequence within a sequence.
            raise ValueError(f'Unexpected field {field}')


class Serializer(metaclass=abc.ABCMeta):
    """
    `Serializer` serializes a :class:`Serializable` object into a format such as JSON, YAML, or others.

    The format depends on the serializer subclass.
    """

    @abc.abstractmethod
    def serialize(
            self,
            val: Serializable,
            fp: typing.IO,
    ):
        """
        Serialize a value `val` into the provided IO object `fp`.
        """
        pass


E = typing.TypeVar('E', bound=enum.Enum)
"""
A type that is a subclass of :class:`enumEnum`.
"""


class Deserializable(metaclass=abc.ABCMeta):
    """
    `Deserializable` knows how to initialize itself
    based on a `dict` with intermediate Python representation.

    See :class:`Serializable` for more info.
    """

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        # Can raise if a required field is missing
        pass

    @classmethod
    @abc.abstractmethod
    def required_fields(cls) -> typing.Sequence[str]:
        # May not be implemented if the class includes a field with oneof Protobuf semantics!
        pass

    @classmethod
    def _all_required_fields_are_present(
            cls,
            values: typing.Mapping[str, typing.Any]
    ) -> bool:
        return all(field in values for field in cls.required_fields())

    @classmethod
    def _complain_about_missing_field(
            cls,
            values: typing.Mapping[str, typing.Any]
    ):
        missing = tuple(filter(lambda f: f not in values, cls.required_fields()))
        raise ValueError(f'{cls.__name__}: missing {len(missing)} required field(s): {missing}')

    @staticmethod
    def _extract_optional_field(
            key: str,
            vals: typing.Mapping[str, typing.Any],
    ) -> typing.Optional[typing.Any]:
        return vals[key] if key in vals else None

    @staticmethod
    def _extract_enum_field(
            key: str,
            clz: typing.Type[E],
            vals: typing.Mapping[str, typing.Any],
    ) -> typing.Optional[E]:
        return clz[vals[key]] if key in vals else None


D = typing.TypeVar('D', bound=Deserializable)
"""
A type that is a subclass of :class:`Deserializable`.
"""


def extract_oneof_scalar(
        clsd: typing.Mapping[str, typing.Type[D]],
        vals: typing.Mapping[str, typing.Any],
) -> typing.Optional[D]:
    for key, cls in clsd.items():
        scalar = extract_message_scalar(key, cls, vals)
        if scalar is not None:
            return scalar
    return None


def extract_message_scalar(
        key: str,
        cls: typing.Type[D],
        vals: typing.Mapping[str, typing.Any],
) -> typing.Optional[D]:
    return cls.from_dict(vals[key]) if key in vals else None


def extract_message_sequence(
        key: str,
        cls: typing.Type[D],
        vals: typing.Mapping[str, typing.Any],
) -> typing.Optional[typing.Sequence[D]]:
    if key in vals:
        val = vals[key]
        if not isinstance(val, typing.Sequence):
            raise ValueError('Bug')  # TODO: improve error handling
        else:
            return [cls.from_dict(item) for item in val]
    else:
        return None


class Deserializer(metaclass=abc.ABCMeta):
    """
    `Deserializer` decodes a :class:`Deserializable` class from a `str` or text IO handle.
    """

    @abc.abstractmethod
    def deserialize(
            self,
            fp: typing.Union[str, io.TextIOBase],
            clz: typing.Type[D],
    ) -> D:
        """
        Decode an instance of deserializable class from the input `fp`.

        :param fp: input to decode either as a `str` or a text IO handle.
        :param clz: type of the class to be created from the input.
        :returns: a new instance of `D` with attributes set based on the `fp`.
        """
        pass
