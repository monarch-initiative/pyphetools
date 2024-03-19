import io
import json
import typing

from .._io import Serializer, Serializable, Deserializer, D
from .._util import CaseConverter, HierarchicalKeyMapper

_PRIMITIVES = {
    bool, int, float, str,
}


def map_dict_keys_case(
        func: typing.Callable[[str], str],
        vals: typing.Union[typing.Mapping[str, typing.Any], typing.Sequence[typing.Any], typing.Any],
) -> typing.Union[typing.Mapping[str, typing.Any], typing.Any]:
    if type(vals) in _PRIMITIVES:
        return vals

    if isinstance(vals, typing.Mapping):
        out = {}
        for key, val in vals.items():
            new_key = func(key)
            if type(val) in _PRIMITIVES:
                new_val = val
            elif isinstance(val, typing.Sequence):
                new_val = [map_dict_keys_case(func, e) for e in val]
            elif isinstance(val, typing.Mapping):
                new_val = map_dict_keys_case(func, val)
            else:
                new_val = val

            out[new_key] = new_val

        return out
    else:
        raise ValueError('Bug')


class JsonSerializer(Serializer):
    """
    A serializer to format :class:`Serializable` objects into JSON format.

    The serializer will convert the field names from snake case used in Python into camel case
    (e.g. `file_attributes` -> `fileAttributes`).
    For the purpose of working with Phenopacket Schema, the serializer will not convert the map keys,
    (e.g. keys of `file_attributes` map).

    See :func:`json.dump` for the accepted keyword arguments.
    """

    def __init__(
            self,
            **kwargs
    ):
        self._kwargs = kwargs
        self._case_converter = CaseConverter()
        self._key_mapper = HierarchicalKeyMapper.ps_v202_mapper()

    def serialize(self, val: Serializable, fp: typing.IO):
        out = {}
        val.to_dict(out)
        mapped = self._key_mapper.remap_mapping(self._case_converter.snake_to_camel, out)
        json.dump(mapped, fp, **self._kwargs)


class JsonDeserializer(Deserializer):
    """
    A deserializer to load :class:`Deserializable` objects from JSON format.

    The deserializer supports reading a JSON with keys
    in both *snake case* (e.g. `file_attributes`) and *camel case* (e.g. `fileAttributes`).
    """

    def __init__(self):
        self._case_converter = CaseConverter()
        self._key_mapper = HierarchicalKeyMapper.ps_v202_mapper()

    def deserialize(
            self,
            fp: typing.Union[str, io.TextIOBase],
            clz: typing.Type[D]) -> D:
        val = self._decode_json_content(fp)

        mapped = self._key_mapper.remap_mapping(self._case_converter.camel_to_snake, val)
        return clz.from_dict(mapped)

    @staticmethod
    def _decode_json_content(fp: typing.Union[str, io.TextIOBase]):

        if isinstance(fp, str):
            val = json.loads(fp)
        elif isinstance(fp, io.TextIOBase):
            val = json.load(fp)
        else:
            raise ValueError(f'`fp` must be a `str` or `io.TextIOBase` but was {type(fp)}')
        return val
