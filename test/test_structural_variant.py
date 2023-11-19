import unittest
from src.pyphetools.creation import StructuralVariant


class TestVariantValidator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        variant = "46,XY.ish del(7)(p14.1)(RP11-816F16-)"
        genotype = "heterozygous"
        gene = "GLI3"
        gene_id = "HGNC:4319"
        sv = StructuralVariant.chromosomal_deletion(cell_contents=variant,
                                                    gene_symbol=gene,
                                                    gene_id=gene_id)
        sv.set_heterozygous()
        cls._variant_interpretation = sv.to_ga4gh_variant_interpretation()

    def test_label(self):
        var_inter = self._variant_interpretation
        variant_descriptor = var_inter.variation_descriptor
        label = variant_descriptor.label
        self.assertEqual("46,XY.ish del(7)(p14.1)(RP11-816F16-)", label)

    def test_zygosity(self):
        variant_descriptor = self._variant_interpretation.variation_descriptor
        allelic_state = variant_descriptor.allelic_state
        self.assertEqual("GENO:0000135", allelic_state.id)
        self.assertEqual("heterozygous", allelic_state.label)

    def test_structural_type(self):
        variant_descriptor = self._variant_interpretation.variation_descriptor
        structural_type = variant_descriptor.structural_type
        self.assertEqual("SO:1000029", structural_type.id)
        self.assertEqual("chromosomal_deletion", structural_type.label)
