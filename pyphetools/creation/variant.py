import abc


class Variant(metaclass=abc.ABCMeta):
    """Superclass for classes that create GA4GH VariantInterpretationObjects"""
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def to_ga4gh_variant_interpretation(self, acmg=None):
        pass