import string
import random
import typing
from ..pp.v202 import AcmgPathogenicityClassification as ACMG202
from ..pp.v202 import GeneDescriptor as GeneDescriptor202
from ..pp.v202 import VariationDescriptor as VariationDescriptor202
from ..pp.v202 import VariantInterpretation as VariantInterpretation202
from ..pp.v202 import MoleculeContext as MoleculeContext202
from ..pp.v202 import OntologyClass as OntologyClass202


from .variant import Variant


class PromoterVariant(Variant):


    def __init__(self,
                 description: str,
                 gene_symbol: str,
                 gene_id: str,
                 sequence_ontology_term: OntologyClass202,
                 genotype: OntologyClass202,
                 variant_id: str=None) -> None:
        if variant_id is None:
            self._variant_id = "var_" + "".join(random.choices(string.ascii_letters, k=25))
        else:
            self._variant_id = variant_id
        self._description = description.strip()
        if gene_symbol is None:
            raise ValueError(f"Need to pass a valid gene symbol!")
        self._gene_symbol = gene_symbol
        if gene_id is None:
            raise ValueError(f"Need to pass a valid HGNC gene id!")
        self._hgnc_id = gene_id
        self._sequence_ontology_term = sequence_ontology_term
        self._genotype = genotype

    def to_ga4gh_variant_interpretation():
        raise NotImplementedError("This method will be deprecated")


    def to_variant_interpretation(self, acmg=None) -> VariantInterpretation202:
        """
        Transform this PromoterVariant object into a VariantInterpretation message (pp.v202 class)
        """
        gene_descriptor = GeneDescriptor202(value_id=self._hgnc_id, symbol=self._gene_symbol)
        vdescriptor = VariationDescriptor202(id=self._variant_id, 
                                             molecule_context=MoleculeContext202.genomic,
                                             gene_context=gene_descriptor,
                                             label=self._description,
                                             structural_type=self._sequence_ontology_term)
        if self._genotype is not None:
            vdescriptor.allelic_state = self._genotype
        acmg_code = Variant._get_acmg_classification(acmg=acmg)
        vinterpretation = VariantInterpretation202(variation_descriptor=vdescriptor, acmg_pathogenicity_classification=acmg_code)
        return vinterpretation


    @staticmethod
    def two_KB_upstream_variant(description: str,
                gene_symbol: str,
                gene_id: str,
                genotype:str = None,
                variant_id=None):
        """
        A sequence variant located within 2KB 5' of a gene.

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = PromoterVariant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001636", label="2KB_upstream_variant")
        return PromoterVariant(description=description,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 sequence_ontology_term=so_term,
                                 genotype=gt_term,
                                 variant_id=variant_id)


    @staticmethod
    def five_KB_upstream_variant(description: str,
                gene_symbol: str,
                gene_id: str,
                genotype: str = None,
                variant_id=None):
        """
        A sequence variant located within 5KB 5' of a gene.

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = Variant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001635", label="5KB_upstream_variant")
        return PromoterVariant(description=description,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 sequence_ontology_term=so_term,
                                 genotype=gt_term,
                                 variant_id=variant_id)


    @staticmethod
    def upstream_transcript_variant(description: str,
                                    gene_symbol: str,
                                    gene_id: str,
                                    genotype: str = None,
                                    variant_id=None):
        """
        A feature variant, where the alteration occurs upstream of the transcript TSS.

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = PromoterVariant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001986", label="upstream_transcript_variant")
        return PromoterVariant(description=description,
                                gene_symbol=gene_symbol,
                                gene_id=gene_id,
                                sequence_ontology_term=so_term,
                                genotype=gt_term,
                                variant_id=variant_id)
    
    @staticmethod
    def upstream_gene_variant(description: str,
                            gene_symbol: str,
                            gene_id: str,
                            genotype: str = None,
                            variant_id=None):
        """
        A sequence variant located 5' of a gene.

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = PromoterVariant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001631", label="upstream_gene_variant")
        return PromoterVariant(description=description,
                                gene_symbol=gene_symbol,
                                gene_id=gene_id,
                                sequence_ontology_term=so_term,
                                genotype=gt_term,
                                variant_id=variant_id)

    