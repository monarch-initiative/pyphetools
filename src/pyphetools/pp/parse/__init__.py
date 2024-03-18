"""
A package to support the (de)serialization of phenopacket schema elements to/from various formats,
such as JSON, YAML, and protobuf.
"""
from . import json
from ._io import Serializer, Serializable, Deserializer, Deserializable
from ._io import extract_message_scalar, extract_message_sequence
from ._pb import FromProtobuf, ToProtobuf
from ._pb import extract_pb_message_scalar, extract_pb_message_seq

__all__ = [
    'Serializer', 'Serializable', 'Deserializer', 'Deserializable',
    'FromProtobuf', 'ToProtobuf',
]
