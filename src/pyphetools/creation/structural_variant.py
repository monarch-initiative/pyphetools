import string
import random
import phenopackets
from .variant import Variant

ACCEPTABLE_GENOMES = {"GRCh37", "GRCh38", "hg19", "hg38"}


class StructuralVariant(Variant):
    """
    This encapsulates variant about a structural variant
    For instance, we may see things like this
    chr7.hg19:g.(35674000_37280000)_(46_111_000_46_598_000)del (fuzzy boundaries)
    chr7.hg19:g(38521704_45810267)del (precise boundaries)
    rsa7p14.1(kit P179)x1
    46,XY.ish del(7)(p14.1)(RP11-816F16-)
    46,XX.ish del(7)(p14.1p14.1)(GLI3-)
    46,XY.ish del(7)(p14.1)(GLI3-)[56]/7p14.1(GLI3x2)[44] (various ICSN or bespoke)
    Our strategy is not to model these variants precisely. Instead, for genotype-phenotype
    analysis, it may be enough to know that these are structural variants and thus
    likely to be complete loss of function.
    So we record something about the variant and add it by hand to the Individual object
    We want to be able to create a GA4GH VariationDescriptor object with the following fields
    - id - required, autogenerate if user provides no id
    - variant (VRS) -- leave this field empty
    - label -- the original contents of the cell, e.g., 46,XY.ish del(7)(p14.1)(RP11-816F16-)
    - gene context -- the gene that is disrupted by the structural variant
    - expressions, empty
    - vcf_record, empty
    - structural type: Ontology Class
    - allelic state: het/hom/emi etc.

    :param cell_contents: the string from the original table that we want to map as a structural variant
    :type cell_contents: str
    :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
    :type gene_symbol: str
    :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
    :type gene_id: str
    :param sequence_ontology_id: An identifier from the Sequence Ontology
    :type sequence_ontology_id: str
    :param sequence_ontology_label: the SO label corresponding to the ID
    :type sequence_ontology_label: str
    :param variant_id: an identifier for the variant, optional
    :type variant_id: str
    """

    def __init__(self, cell_contents,
                 gene_symbol,
                 gene_id,
                 sequence_ontology_id,
                 sequence_ontology_label,
                 variant_id: None):
        super().__init__()
        if variant_id is None:
            self._variant_id = "var_" + "".join(random.choices(string.ascii_letters, k=25))
        else:
            self._variant_id = variant_id
        self._label = cell_contents.strip()
        if gene_symbol is None:
            raise ValueError(f"Need to pass a valid gene symbol!")
        self._gene_symbol = gene_symbol
        if gene_id is None:
            raise ValueError(f"Need to pass a valid HGNC gene id!")
        self._hgnc_id = gene_id
        self._so_id = sequence_ontology_id
        self._so_label = sequence_ontology_label
        self._genotype = None

    def to_ga4gh_variant_interpretation(self, acmg=None):
        """
        Transform this Variant object into a "variantInterpretation" message of the GA4GH Phenopacket schema
        """
        vdescriptor = phenopackets.VariationDescriptor()
        vdescriptor.id = self._variant_id
        vdescriptor.gene_context.value_id = self._hgnc_id
        vdescriptor.gene_context.symbol = self._gene_symbol
        vdescriptor.label = self._label
        vdescriptor.molecule_context = phenopackets.MoleculeContext.genomic
        if self._genotype is not None:
            if self._genotype == 'heterozygous':
                vdescriptor.allelic_state.id = "GENO:0000135"
                vdescriptor.allelic_state.label = "heterozygous"
            elif self._genotype == 'homozygous':
                vdescriptor.allelic_state.id = "GENO:0000136"
                vdescriptor.allelic_state.label = "homozygous"
            elif self._genotype == 'hemizygous':
                vdescriptor.allelic_state.id = "GENO:0000134"
                vdescriptor.allelic_state.label = "hemizygous"
            else:
                print(f"Did not recognize genotype {self._genotype}")
        vdescriptor.structural_type.id = self._so_id
        vdescriptor.structural_type.label = self._so_label
        vinterpretation = phenopackets.VariantInterpretation()
        if acmg is not None:
            if acmg.lower() == 'benign':
                vinterpretation.acmgPathogenicityClassification = phenopackets.AcmgPathogenicityClassification.BENIGN
            elif acmg.lower == 'likely benign' or acmg.lower() == 'likely_benign':
                vinterpretation.acmgPathogenicityClassification = phenopackets.AcmgPathogenicityClassification.LIKELY_BENIGN
            elif acmg.lower == 'uncertain significance' or acmg.lower() == 'uncertain_significance':
                vinterpretation.acmgPathogenicityClassification = phenopackets.AcmgPathogenicityClassification.UNCERTAIN_SIGNIFICANCE
            elif acmg.lower == 'likely pathogenic' or acmg.lower() == 'likely_pathogenic':
                vinterpretation.acmgPathogenicityClassification = phenopackets.AcmgPathogenicityClassification.LIKELY_PATHOGENIC
            elif acmg.lower == 'pathogenic' or acmg.lower() == 'pathogenic':
                vinterpretation.acmgPathogenicityClassification = phenopackets.AcmgPathogenicityClassification.PATHOGENIC
            else:
                print(f"Warning- did not recognize ACMG category {acmg}")
        vinterpretation.variation_descriptor.CopyFrom(vdescriptor)
        return vinterpretation

    # provide static constructors for most important structural variation types

    @staticmethod
    def chromosomal_deletion(cell_contents,
                             gene_symbol,
                             gene_id,
                             variant_id=None):
        """
        create a StructuralVariant object for a chromosomal deletion

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        return StructuralVariant(cell_contents=cell_contents,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 sequence_ontology_id="SO:1000029",
                                 sequence_ontology_label="chromosomal_deletion",
                                 variant_id=variant_id)

    @staticmethod
    def chromosomal_duplication(cell_contents,
                                gene_symbol,
                                gene_id,
                                variant_id=None):
        """
        create a StructuralVariant object for a chromosomal duplication

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        return StructuralVariant(cell_contents=cell_contents,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 sequence_ontology_id="SO:1000037",
                                 sequence_ontology_label="chromosomal_duplication",
                                 variant_id=variant_id)

    @staticmethod
    def chromosomal_inversion(cell_contents,
                              gene_symbol,
                              gene_id,
                              genotype,
                              variant_id=None):
        """
        create a StructuralVariant object for a chromosomal inversion

        :param cell_contents: the string from the original table that we want to map as a structural variant
        :type cell_contents: str
        :param gene_symbol: the gene affected by the structural variant, e.g., GLI3
        :type gene_symbol: str
        :param gene_id: the identifier (using HGNC) of the gene, e.g., GLI3 is HGNC:4319
        :type gene_id: str
        :param genotype: Genotype (heterozygous, homozygous, hemizygous) of this variant call
        :type genotype: str
        :param variant_id: an identifier for the variant
        :type variant_id: str, optional
        """
        return StructuralVariant(cell_contents=cell_contents,
                                 gene_symbol=gene_symbol,
                                 gene_id=gene_id,
                                 sequence_ontology_id="SO:1000030",
                                 sequence_ontology_label="chromosomal_inversion",
                                 variant_id=variant_id)
