import abc


class PhenopacketValidator(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def validate_phenopacket(self, phenopacket):
        pass