import abc


class Variant(metaclass=abc.ABCMeta):
    """Superclass for classes that create GA4GH VariantInterpretationObjects"""
    
    def __init__(self):
        self._genotype = None

    @abc.abstractmethod
    def to_ga4gh_variant_interpretation(self, acmg=None):
        pass
    
    def set_heterozygous(self):
        self._genotype = 'heterozygous'
    
    def set_homozygous(self):
        self._genotype = 'homozygous'
        
    def set_hemizygous(self):
        self._genotype = 'hemizygous'
        
    def set_genotype(self, gt):
        genotype = gt.lower()
        if genotype not in {'heterozygous', 'homozygous', 'hemizygous'}:
            raise ValueError(f"Unrecognized genotype {gt}")
        self._genotype = genotype