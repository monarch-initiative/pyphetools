import abc

from .parse import Serializable, Deserializable


# - We do not validate the values, just their presence and type


class MessageMixin(Serializable, Deserializable, metaclass=abc.ABCMeta):

    # MANDATORY
    @abc.abstractmethod
    def __eq__(self, other):
        pass
