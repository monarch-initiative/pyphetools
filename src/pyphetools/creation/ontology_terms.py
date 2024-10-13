from ..pp.v202 import OntologyClass as OntologyClass202
import typing


class OntologyTerms:
    """
    Convenience class that offers Builders for commonly used OntologyClass objects.
    """

    @staticmethod
    def heterozygous() -> OntologyClass202:
        """
        Sequence Ontology class for heterozygous
        """
        return OntologyClass202(id="GENO:0000135", label="heterozygous")
    
    @staticmethod
    def homozygous() -> OntologyClass202:
        """
        Sequence Ontology class for homozygous
        """
        return OntologyClass202(id="GENO:0000136", label="homozygous")
    
    @staticmethod
    def hemizygous() -> OntologyClass202:
        """
        Sequence Ontology class for hemizygous
        """
        return OntologyClass202(id="GENO:0000134", label="hemizygous")
    
    ## Onset terms
    @staticmethod
    def congenital_onset() -> OntologyClass202:
        """
        HPO class for Congenital onset
        """
        return OntologyClass202(id="HP:0003577", label="Congenital onset")
    
    
