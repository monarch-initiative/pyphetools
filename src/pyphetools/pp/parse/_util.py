import re
# import typing


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
        else:
            return tokens[0] + ''.join(map(lambda s: s.title(), tokens[1:]))


# class HierarchicalKeyMapper:
#
#     _PRIMITIVES = {
#         bool, int, float, str,
#     }
#
#     def __init__(
#             self,
#             blacklist: typing.Iterable[str],
#     ):
#         self._blist = set(blacklist)
#
#     def remap(
#             self,
#             func: typing.Callable[[str], str],
#             vals: typing.Union[typing.Mapping[str, typing.Any], typing.Sequence[typing.Any], typing.Any],
#     ):
#         if type(vals) in HierarchicalKeyMapper._PRIMITIVES:
#             return vals
#
#         if isinstance(vals, typing.Mapping):
#             out = {}
#             for key, val in vals.items():
#                 new_key = key if key in self._blist else func(key)
#
#                 if type(val) in HierarchicalKeyMapper._PRIMITIVES:
#                     new_val = val
#                 elif isinstance(val, typing.Sequence):
#                     new_val = [self.remap(func, e) for e in val]
#                 elif isinstance(val, typing.Mapping):
#                     new_val = self.remap(func, val)
#                 else:
#                     new_val = val
#
#                 out[new_key] = new_val
#
#             return out
#         else:
#             raise ValueError('Bug')
#
#     def _submap(
#             self,
#             func: typing.Callable[[str], str],
#             vals: typing.Union[typing.Mapping[str, typing.Any], typing.Sequence[typing.Any], typing.Any],
#
#     ):
#         pass
