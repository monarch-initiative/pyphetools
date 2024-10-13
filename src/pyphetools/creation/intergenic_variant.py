import string
import random
import typing
import re
from ..pp.v202 import GeneDescriptor as GeneDescriptor202, VcfRecord
from ..pp.v202 import MoleculeContext as MoleculeContext202
from ..pp.v202 import OntologyClass as OntologyClass202
from ..pp.v202 import VariationDescriptor as VariationDescriptor202
from ..pp.v202 import VariantInterpretation as VariantInterpretation202
from ..pp.v202 import VcfRecord as VcfRecord202

from .variant import Variant

chromosome_d = {
    "NC_000001.11": "chr1",
    "NC_000002.12": "chr2",
    "NC_000003.12": "chr3",
    "NC_000004.12": "chr4",
    "NC_000005.10": "chr5",
    "NC_000006.12": "chr6",
    "NC_000007.14": "chr7",
    "NC_000008.11": "chr8",
    "NC_000009.12": "chr9",
    "NC_000010.11": "chr10",
    "NC_000011.10": "chr11",
    "NC_000012.12": "chr12",
    "NC_000013.11": "chr13",
    "NC_000014.9": "chr14",
    "NC_000015.10": "chr15",
    "NC_000016.10": "chr16",
    "NC_000017.11": "chr17",
    "NC_000018.10": "chr18",
    "NC_000019.10": "chr19",
    "NC_000020.11": "chr20",
    "NC_000021.9": "chr21",
    "NC_000022.11": "chr22",
    "NC_000023.11": "chrX",
    "NC_000024.10": "chrY",
}


class IntergenicVariant(Variant):
    """
    This class provides a means of adding information about variants that cannot be
    annotated with transcript-hased HGVS expressions, but for which we do have
    exact genomic positions. For instance, a promoter variant (5' to the transcription
    start site) cannot be expressed by negative positions with respect to the transcript accession number.
    """

    def __init__(self,
                 description: str,
                 gene_symbol: str,
                 gene_id: str,
                 vcf_record: VcfRecord,
                 sequence_ontology_term: OntologyClass202,
                 genotype: OntologyClass202,
                 variant_id: str = None) -> None:
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
        self._vcf_record = vcf_record
        self._sequence_ontology_term = sequence_ontology_term
        self._genotype = genotype

    def to_ga4gh_variant_interpretation(self):
        raise NotImplementedError("This method will be deprecated")

    def to_variant_interpretation(self, acmg=None) -> VariantInterpretation202:
        """
        Transform this PromoterVariant object into a VariantInterpretation message (pp.v202 class)
        """
        gene_descriptor = GeneDescriptor202(value_id=self._hgnc_id, symbol=self._gene_symbol)
        vdescriptor = VariationDescriptor202(id=self._variant_id,
                                             molecule_context=MoleculeContext202.genomic,
                                             description=self._description,
                                             gene_context=gene_descriptor,
                                             vcf_record=self._vcf_record,
                                             label=self._description,
                                             structural_type=self._sequence_ontology_term)
        if self._genotype is not None:
            vdescriptor.allelic_state = self._genotype
        acmg_code = Variant._get_acmg_classification(acmg=acmg)
        vinterpretation = VariantInterpretation202(variation_descriptor=vdescriptor,
                                                   acmg_pathogenicity_classification=acmg_code)
        return vinterpretation

    @staticmethod
    def _hgvs_g_to_vcf(hgvs_g: str) -> VcfRecord:
        """
        :param hgvs_g: A string such as NC_000001.11:g.75749509G>A representing a small intergenic (e.g., promoter) var
        :type hgvs_g: str
        """
        fields = hgvs_g.split(":")
        chrom_string = fields[0]
        if chrom_string in chromosome_d:
            chrom_string = chromosome_d[chrom_string]
        var = fields[1]
        if not var.startswith("g."):
            raise ValueError(f"Invalid HGVS (variant does not start with g.): {hgvs_g}")
        var = var[2:]
        var_re = r'(\d+)([ACGT]+)>([ACGT]+)'
        match = re.match(var_re, var)
        if match:
            pos = int(match.group(1))
            ref = match.group(2)
            alt = match.group(3)
            return VcfRecord202(genome_assembly="hg38",
                                chrom=chrom_string,
                                pos=pos,
                                ref=ref,
                                alt=alt)
        else:
            raise ValueError(f"Invalid HGVS (could not parse variant): {hgvs_g}")

    @staticmethod
    def two_KB_upstream_variant(description: str,
                                gene_symbol: str,
                                gene_id: str,
                                hgvs_g: str,
                                genotype: str = None,
                                variant_id=None):
        """
        A sequence variant located within 2KB 5' of a gene.

        :param description: the string from the original table that we want to map as a structural variant
        :type description: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param hgvs_g: A string such as NC_000001.11:g.75749509G>A representing a small intergenic (e.g., promoter) var
        :type hgvs_g: str
        :param genotype: One of 'heterozygous', 'homozygous', 'hemizygous'
        :type genotype: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = IntergenicVariant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001636", label="2KB_upstream_variant")
        vcf_rec = IntergenicVariant._hgvs_g_to_vcf(hgvs_g=hgvs_g)
        return IntergenicVariant(description=description,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 vcf_record=vcf_rec,
                                 sequence_ontology_term=so_term,
                                 genotype=gt_term,
                                 variant_id=variant_id)

    @staticmethod
    def five_KB_upstream_variant(description: str,
                                 gene_symbol: str,
                                 gene_id: str,
                                 hgvs_g: str,
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
        :param hgvs_g: A string such as NC_000001.11:g.75749509G>A representing a small intergenic (e.g., promoter) var
        :type hgvs_g: str
        :param genotype: One of 'heterozygous', 'homozygous', 'hemizygous'
        :type genotype: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = Variant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001635", label="5KB_upstream_variant")
        vcf_rec = IntergenicVariant._hgvs_g_to_vcf(hgvs_g=hgvs_g)
        return IntergenicVariant(description=description,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 vcf_record=vcf_rec,
                                 sequence_ontology_term=so_term,
                                 genotype=gt_term,
                                 variant_id=variant_id)

    @staticmethod
    def upstream_transcript_variant(description: str,
                                    gene_symbol: str,
                                    gene_id: str,
                                    hgvs_g: str,
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
        :param hgvs_g: A string such as NC_000001.11:g.75749509G>A representing a small intergenic (e.g., promoter) var
        :type hgvs_g: str
        :param genotype: One of 'heterozygous', 'homozygous', 'hemizygous'
        :type genotype: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = IntergenicVariant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001986", label="upstream_transcript_variant")
        vcf_rec = IntergenicVariant._hgvs_g_to_vcf(hgvs_g=hgvs_g)
        return IntergenicVariant(description=description,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 vcf_record=vcf_rec,
                                 sequence_ontology_term=so_term,
                                 genotype=gt_term,
                                 variant_id=variant_id)

    @staticmethod
    def upstream_gene_variant(description: str,
                              gene_symbol: str,
                              gene_id: str,
                              hgvs_g: str,
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
        :param hgvs_g: A string such as NC_000001.11:g.75749509G>A representing a small intergenic (e.g., promoter) var
        :type hgvs_g: str
        :param genotype: One of 'heterozygous', 'homozygous', 'hemizygous'
        :type genotype: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        gt_term = IntergenicVariant._get_genotype_term(genotype=genotype)
        so_term = OntologyClass202(id="SO:0001631", label="upstream_gene_variant")
        vcf_rec = IntergenicVariant._hgvs_g_to_vcf(hgvs_g=hgvs_g)
        return IntergenicVariant(description=description,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 vcf_record=vcf_rec,
                                 sequence_ontology_term=so_term,
                                 genotype=gt_term,
                                 variant_id=variant_id)
