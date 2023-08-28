import abc


class Variant(metaclass=abc.ABCMeta):
    """Superclass for classes that create GA4GH VariantInterpretationObjects"""
    
    def __init__(self):
        self._genotype = None

    @abc.abstractmethod
    def to_ga4gh_variant_interpretation(self, acmg=None):
        """
        Embed the variant object into a GA4GH Genomic Interpretation obbject (abstract)

        :param acmg: ACMG pathogenicity level (default: None)
        """
        pass
    
    def set_heterozygous(self):
        """
        Assign heterozygous allele status to this variant

        """
        self._genotype = 'heterozygous'
    
    def set_homozygous(self):
        """
        Assign homozygous allele status to this variant

        """
        self._genotype = 'homozygous'
        
    def set_hemizygous(self):
        """
        Assign hemizygous allele status to this variant

        """
        self._genotype = 'hemizygous'
        
    def set_genotype(self, gt):
        """
        Assign an allele status to this variant

        :param gt: The genotype (allele status) of this variant

        """
        genotype = gt.lower()
        if genotype not in {'heterozygous', 'homozygous', 'hemizygous'}:
            raise ValueError(f"Unrecognized genotype {gt}")
        self._genotype = genotype