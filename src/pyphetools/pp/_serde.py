import abc


class Serializer(metaclass=abc.ABCMeta):
    # Can be JSON, YAML, Protobuf, anything
    pass


class Deserializer(metaclass=abc.ABCMeta):
    pass


class Serializable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def serialize(self, serializer: Serializer):
        pass


class Deserializable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def deserialize(self, deserializer: Deserializer):
        pass
