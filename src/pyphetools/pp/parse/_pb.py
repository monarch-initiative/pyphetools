import abc
import typing

from google.protobuf.message import Message


class ToProtobuf(metaclass=abc.ABCMeta):
    """
    A mixin for data classes that can encode themselves into some protobuf bytes.

    **Example**

    Let's create an example subject:

    >>> from pyphetools.pp.v202 import Individual
    >>> i = Individual(id='example.id', alternate_ids=['other', 'identifiers'])

    Now we can serialize the individual into a file or, for the purpose of this test, into :class:`io.BytesIO` buffer:

    >>> import io
    >>> buf = io.BytesIO()

    >>> i.dump_pb(buf)

    >>> buf.getvalue()
    b'\\n\\nexample.id\\x12\\x05other\\x12\\x0bidentifiers'
    """

    @abc.abstractmethod
    def to_message(self) -> Message:
        """
        Get a protobuf representation of the class.
        """
        pass

    def dump_pb(self, fp: typing.BinaryIO):
        """
        Write the protobuf representation of the class into the provided `fp` byte handle.
        """
        msg = self.to_message()
        fp.write(msg.SerializeToString())


class FromProtobuf(metaclass=abc.ABCMeta):
    """
    A mixin for data classes/types that can be created from some protobuf bytes.

    In general, the deserialization first constructs an intermediate Protobuf :class:`Message`. The message is then
    mapped into the actual class.

    **Example**

    Let's load example protobuf file at the following location:

    >>> import os
    >>> fpath_pb = os.path.join('test', 'data', 'pp', 'retinoblastoma.pb')


    The file contains a v2.0.2 phenopacket. Let's import the `Phenopacket` class and load the file:

    >>> from pyphetools.pp.v202 import Phenopacket
    >>> with open(fpath_pb, 'rb') as fh:
    ...   pp = Phenopacket.from_pb(fh)

    Now we have a phenopacket that we can work with:

    >>> pp.id
    'example.retinoblastoma.phenopacket.id'

    """

    @classmethod
    @abc.abstractmethod
    def message_type(cls) -> typing.Type[Message]:
        """
        Get the type of the protobuf element that this class can be decoded from.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_message(cls, msg: Message):
        """
        Decode the message into a new instance of this class.
        """
        pass

    @classmethod
    def from_pb(
            cls,
            fp: typing.BinaryIO,
    ):
        """
        Create an instance from some bytes read from `pb`.
        The bytes are expected to correspond to the state of the message.
        """
        msg_type = cls.message_type()
        msg = msg_type()
        msg.MergeFromString(fp.read())

        return cls.from_message(msg)

    @classmethod
    def complain_about_incompatible_msg_type(
            cls,
            msg: Message,
    ):
        """
        A utility method for user-friendly complaint regarding attempting to decode from incompatible type.
        """
        raise ValueError(f'Cannot decode {cls} from {type(msg)}')


FP = typing.TypeVar('FP', bound=FromProtobuf)
"""
A type that is a subclass of :class:`FromProtobuf`.
"""


def extract_pb_oneof_scalar(
        oneof_group: str,
        clsd: typing.Mapping[str, typing.Type[FP]],
        msg: Message,
) -> typing.Optional[FP]:
    key = msg.WhichOneof(oneof_group)
    if key is not None:
        cls = clsd[key]
        return extract_pb_message_scalar(key, cls, msg)
    else:
        return None


def extract_pb_message_scalar(
        key: str,
        cls: typing.Type[FP],
        msg: Message,
) -> typing.Optional[FP]:
    if msg.HasField(key):
        return cls.from_message(getattr(msg, key))
    else:
        return None


def extract_pb_message_seq(
        key: str,
        cls: typing.Type[FP],
        msg: Message,
) -> typing.Iterable[FP]:
    return (cls.from_message(i) for i in getattr(msg, key))
