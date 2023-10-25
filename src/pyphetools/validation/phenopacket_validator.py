import abc


class PhenopacketValidator(metaclass=abc.ABCMeta):
    """
    Abstract super class for classes that validate phenopackets
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def validate_phenopacket(self, phenopacket):
        pass