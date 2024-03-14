import abc
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
            out: typing.Union[typing.MutableMapping[str, typing.Any], typing.MutableSequence[typing.Any]],
    ):
        if field is None:
            pass

        elif type(field) in Serializable._PRIMITIVES:
            if isinstance(out, typing.MutableMapping):
                out[name] = field
            elif isinstance(out, typing.MutableSequence):
                out.append(field)
            else:
                raise ValueError('Bug')

        elif isinstance(field, typing.Sequence):
            seq = []
            for subfield in field:
                Serializable._put_field_to_mapping(name, subfield, seq)
            if isinstance(out, typing.MutableMapping):
                out[name] = seq
            else:
                raise ValueError('Bug')

        elif isinstance(field, typing.Mapping):
            # I'm not sure if this should be turned into an object or something else.
            raise NotImplementedError('Implement me!')  # TODO: implement!

        elif isinstance(field, Serializable):
            write_msg_to_dict(name, field, out)

        else:
            raise ValueError('Unexpected field')


def write_msg_to_dict(
        key: str,
        val: typing.Optional[Serializable],
        dest: typing.MutableMapping[str, typing.Any],
):
    if val is not None:
        out = {}
        val.to_dict(out)
        dest[key] = out


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


class Deserializable(metaclass=abc.ABCMeta):
    """
    `Deserializable` knows how to initialize itself
    based on a `dict` with intermediate Python representation.

    See :class:`Serializable` for more info.
    """

    @staticmethod
    @abc.abstractmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        # Can raise if a required field is missing
        pass

    @staticmethod
    def _extract_optional_field(
            key: str,
            vals: typing.Mapping[str, typing.Any],
    ) -> typing.Optional[typing.Any]:
        return vals[key] if key in vals else None


D = typing.TypeVar('D', bound=Deserializable)
"""
A type that is subclass of :class:`Deserializable`.
"""


def extract_message_mixin(
        key: str,
        cls: typing.Type[D],
        vals: typing.Mapping[str, typing.Any],
) -> typing.Optional[D]:
    return cls.from_dict(vals[key]) if key in vals else None


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
