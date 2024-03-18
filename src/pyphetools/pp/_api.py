import abc

from .parse import Serializable, Deserializable, FromProtobuf, ToProtobuf


# TODO:
# - There is a problem with map<string, string> because it is represented as a JSON object
#    and the case of keys will be changed during write.
# - We do not validate the values, just their presence and type


class MessageMixin(Serializable, Deserializable, FromProtobuf, ToProtobuf,
                   metaclass=abc.ABCMeta):

    # MANDATORY
    @abc.abstractmethod
    def __eq__(self, other):
        pass
