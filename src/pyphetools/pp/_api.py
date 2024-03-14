import abc
import typing

from ._serde import Serializable, Deserializable, Deserializer, Serializer


# - The message should know how to write itself to into a Serializer and read itself from deserializer.
# - Init must take all mandatory values
# - We do not validate the values, just their presence and type


class MessageMixin(Serializable, Deserializable, metaclass=abc.ABCMeta):
    _PRIMITIVES = {
        bool, int, float, str,
    }

    @staticmethod
    @abc.abstractmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        # Can raise if a required field is missing
        pass

    @staticmethod
    @abc.abstractmethod
    def field_names() -> typing.Iterable[str]:
        pass

    def to_dict(self,
                out: typing.MutableMapping[str, typing.Any]):
        for name in self.field_names():
            field = getattr(self, name)
            MessageMixin._put_field_to_mapping(name, field, out)

    @staticmethod
    def _put_field_to_mapping(
            name: str,
            field: typing.Optional[typing.Any],
            out: typing.Union[typing.MutableMapping[str, typing.Any], typing.MutableSequence[typing.Any]],
    ):
        if field is None:
            pass

        elif type(field) in MessageMixin._PRIMITIVES:
            if isinstance(out, typing.MutableMapping):
                out[name] = field
            elif isinstance(out, typing.MutableSequence):
                out.append(field)
            else:
                raise ValueError('Bug')

        elif isinstance(field, typing.Iterable):
            seq = []
            for subfield in field:
                MessageMixin._put_field_to_mapping(name, subfield, seq)
            if isinstance(out, typing.MutableMapping):
                out[name] = seq
            else:
                raise ValueError('Bug')

        elif isinstance(field, MessageMixin):
            write_msg_to_dict(name, field, out)

        else:
            raise ValueError('Unexpected field')

    # MANDATORY
    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @staticmethod
    def _extract_optional_field(key: str,
                                vals: typing.Mapping[str, typing.Any],
                                ) -> typing.Optional[typing.Any]:
        return vals[key] if key in vals else None

    def serialize(self, serializer: Serializer):
        vals = {}
        self.to_dict(vals)
        for k, v in vals.items():
            # v can be:
            # - primitive
            # - messageMixin
            # - sequence
            # - mapping
            print(f'{k}: {v}')

    def deserialize(self, deserializer: Deserializer):
        pass


def write_msg_to_dict(
        key: str,
        val: typing.Optional[MessageMixin],
        dest: typing.MutableMapping[str, typing.Any],
):
    if val is not None:
        out = {}
        val.to_dict(out)
        dest[key] = out


MessageMixinOrSubclass = typing.TypeVar('MessageMixinOrSubclass', bound=MessageMixin)


def extract_message_mixin(
        key: str,
        cls: typing.Type[MessageMixinOrSubclass],
        vals: typing.Mapping[str, typing.Any],
) -> typing.Optional[MessageMixinOrSubclass]:
    return cls.from_dict(vals[key]) if key in vals else None
