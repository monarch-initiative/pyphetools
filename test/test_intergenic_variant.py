import pytest

from pyphetools.creation import IntergenicVariant


class TestIntergenicVariant:

    def test_two_KB_upstream_variant(self):
        cyp21a2_description = "NM_000500.7(CYP21A2):c.-113G>A"
        cyp21a2_symbol = "CYP21A2"
        cyp21a2_hgnc_id = "HGNC:2600"
        hgvs_g = "NC_000006.12:g.32038310G>A"
        var = IntergenicVariant.two_KB_upstream_variant(description=cyp21a2_description,
                                                        gene_symbol=cyp21a2_symbol,
                                                        gene_id=cyp21a2_hgnc_id,
                                                        hgvs_g=hgvs_g,
                                                        genotype="heterozygous",
                                                        variant_id="id.1")
        assert var is not None
        var_202 = var.to_variant_interpretation()
        v_desc = var_202.variation_descriptor
        assert v_desc.description == cyp21a2_description
        allelic_state = v_desc.allelic_state
        assert allelic_state.label == "heterozygous"
        assert allelic_state.id == "GENO:0000135"
        gene_desc = v_desc.gene_context
        assert gene_desc.value_id == cyp21a2_hgnc_id
        assert gene_desc.symbol == cyp21a2_symbol
        vcf_record = v_desc.vcf_record
        assert vcf_record is not None
        assert vcf_record.genome_assembly == "hg38"
        assert vcf_record.chrom == "chr6"
        assert vcf_record.pos == 32038310
        assert vcf_record.ref == "G"
        assert vcf_record.alt == "A"
        assert v_desc.structural_type.id == "SO:0001636"
        assert v_desc.structural_type.label == "2KB_upstream_variant"

    def test_five_KB_upstream_variant(self):
        cyp21a2_description = "NM_000500.7(CYP21A2):c.-3113G>A" # made up variant
        cyp21a2_symbol = "CYP21A2"
        cyp21a2_hgnc_id = "HGNC:2600"
        hgvs_g = "NC_000006.12:g.32038010G>A"
        var = IntergenicVariant.five_KB_upstream_variant(description=cyp21a2_description,
                                                        gene_symbol=cyp21a2_symbol,
                                                        gene_id=cyp21a2_hgnc_id,
                                                        hgvs_g=hgvs_g,
                                                        genotype="heterozygous",
                                                        variant_id="id.1")
        assert var is not None
        var_202 = var.to_variant_interpretation()
        v_desc = var_202.variation_descriptor
        assert v_desc.description == cyp21a2_description
        allelic_state = v_desc.allelic_state
        assert allelic_state.label == "heterozygous"
        assert allelic_state.id == "GENO:0000135"
        gene_desc = v_desc.gene_context
        assert gene_desc.value_id == cyp21a2_hgnc_id
        assert gene_desc.symbol == cyp21a2_symbol
        vcf_record = v_desc.vcf_record
        assert vcf_record is not None
        assert vcf_record.genome_assembly == "hg38"
        assert vcf_record.chrom == "chr6"
        assert vcf_record.pos == 32038010
        assert vcf_record.ref == "G"
        assert vcf_record.alt == "A"
        assert v_desc.structural_type.id == "SO:0001635"
        assert v_desc.structural_type.label == "5KB_upstream_variant"


