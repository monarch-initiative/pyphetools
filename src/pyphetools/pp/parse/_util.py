import re
import typing


class CaseConverter:
    # Not part of the public API!

    def __init__(self):
        self._camel_to_snake = re.compile(r'(?<!^)(?=[A-Z])')


    def camel_to_snake(self, payload: str) -> str:
        return self._camel_to_snake.sub('_', payload).lower()

    @staticmethod
    def snake_to_camel(payload: str) -> str:
        tokens = payload.split('_')
        if len(tokens) == 0:
            return ''
        elif len(tokens) == 1:
            return payload
        else:
            return tokens[0] + ''.join(map(lambda s: s.title(), tokens[1:]))


PS_v202_BLACKLIST = (
    'file_attributes', 'individual_to_file_identifiers', 'individual_to_sample_identifiers',
    'fileAttributes', 'individualToFileIdentifiers', 'individualToSampleIdentifiers',
)


class HierarchicalKeyMapper:
    """
    `HierarchicalKeyMapper` takes a sequence or a mapping of primitive Python types e.g. lists of dicts, or dicts of dicts,
    and applies a remapping function `func` on the mapping keys, unless the enclosing element key is in a blacklist.

    The mapper takes either a sequence of things via :attr:`remap_sequence` or :attr:`remap_mapping` and applies `func`
    recursively.

    .. note::

      This is *not* a definitive solution, it only works with Phenopacket Schema where we only have `map<string, string>`.

    :param blacklist: an iterable of `str` with names of keys whose sub-keys should not be subject
      of the remapping function.
    """

    _PRIMITIVES = {
        bool, int, float, str,
    }

    @staticmethod
    def ps_v202_mapper():
        """
        Create a key mapper for remapping elements of Phenopacket Schema `v2.0.2`.
        """
        return HierarchicalKeyMapper(PS_v202_BLACKLIST)

    def __init__(
            self,
            blacklist: typing.Iterable[str],
    ):
        self._blist = set(blacklist)

    def remap_sequence(
            self,
            func: typing.Callable[[str], str],
            vals: typing.Sequence[typing.Any],
            ) -> typing.Sequence[typing.Any]:
        return self._do_sequence(func, vals)

    def remap_mapping(
            self,
            func: typing.Callable[[str], str],
            vals: typing.Mapping[str, typing.Any],
    ) -> typing.Mapping[str, typing.Any]:
        return self._do_mapping(func, vals, update=True)

    def _do_mapping(
            self,
            func: typing.Callable[[str], str],
            vals: typing.Mapping[str, typing.Any],
            update: bool = True,
    ) -> typing.Mapping[str, typing.Any]:
        out = {}

        for key, val in vals.items():
            if type(val) in HierarchicalKeyMapper._PRIMITIVES:
                new_key = func(key) if update else key
            else:
                new_key = func(key) if update else key
                if isinstance(val, typing.Sequence):
                    val = self._do_sequence(func, val)
                elif isinstance(val, typing.Mapping):
                    update_next = key not in self._blist
                    val = self._do_mapping(func, val, update_next)
                else:
                    raise ValueError(f'Value under {key} was neither a primitive nor a sequence or mapping: {type(val)}')

            out[new_key] = val

        return out

    def _do_sequence(
            self,
            func: typing.Callable[[str], str],
            vals: typing.Sequence[typing.Any],
    ) -> typing.Sequence[typing.Any]:
        out = []

        for i, val in enumerate(vals):
            if type(val) in HierarchicalKeyMapper._PRIMITIVES:
                pass
            else:
                if isinstance(val, typing.Sequence):
                    val = self._do_sequence(func, val)
                elif isinstance(val, typing.Mapping):
                    val = self._do_mapping(func, val, update=True)
                else:
                    raise ValueError(f'Value #{i} was neither a primitive nor a sequence or mapping: {type(val)}')

            out.append(val)

        return out
