import unittest
from src.pyphetools.creation import HpTerm, AllelicRequirement
from src.pyphetools.validation import ValidationResultBuilder



class TestValidationResult(unittest.TestCase):

    def test_redundant(self):
        """
        The function "redundant" in the builder should set the ErrorLevel to "WARNING"
        """
        term = HpTerm(hpo_id="HP:0000123", label="Fake label")
        term2 = HpTerm(hpo_id="HP:000987", label="Ancestor")
        validation_result = ValidationResultBuilder(
            phenopacket_id="id1"
        ).redundant_term(ancestor_term=term2, descendent_term=term).build()
        self.assertEqual("id1", validation_result.id)
        self.assertTrue(validation_result.is_warning())
        self.assertEqual("REDUNDANT", validation_result.category)
        term = validation_result.term
        self.assertIsNotNone(term)
        self.assertEqual("HP:000987", term.id)
        self.assertEqual("Ancestor", term.label)

    def test_not_measured(self):
        vresult = ValidationResultBuilder(
            phenopacket_id="id2"
        ).not_measured(HpTerm(hpo_id="HP:0012345", label="Something")).build()
        self.assertEqual("INFORMATION", vresult.error_level)
        self.assertEqual("NOT_MEASURED", vresult.category)

    def test_allele_count_mono_allelic(self):
        vresult = ValidationResultBuilder("id3").incorrect_allele_count(allelic_requirement=AllelicRequirement.MONO_ALLELIC, observed_alleles=2).build()
        self.assertEqual("ERROR", vresult.error_level)
        self.assertEqual("INCORRECT_ALLELE_COUNT", vresult.category)
        self.assertEqual("Expected one allele for monoallelic but got 2 alleles", vresult.message)

    def test_allele_count_bi_allelic(self):
        vresult = ValidationResultBuilder("id3").incorrect_allele_count(allelic_requirement=AllelicRequirement.BI_ALLELIC, observed_alleles=1).build()
        self.assertEqual("ERROR", vresult.error_level)
        self.assertEqual("INCORRECT_ALLELE_COUNT", vresult.category)
        self.assertEqual("Expected two alleles for biallelic but got 1 alleles", vresult.message)

    def test_insufficient_hpo(self):
        vresult = ValidationResultBuilder("id7").insufficient_hpos(min_hpo=2, n_hpo=1).build()
        self.assertEqual("ERROR", vresult.error_level)
        self.assertEqual("INSUFFICIENT_HPOS", vresult.category)
        self.assertEqual("Minimum HPO terms required 2 but only 1 found", vresult.message)

    def test_observed_and_excluded_is_unfixable(self):
        vresult = ValidationResultBuilder("id3").observed_and_excluded_term(term=HpTerm(hpo_id="HP:0012345", label="Something")).build()
        self.assertEqual("ERROR", vresult.error_level)
        self.assertEqual("OBSERVED_AND_EXCLUDED", vresult.category)
        self.assertTrue(vresult.is_unfixable_error())

    def test_conflict_is_not_unfixable(self):
        vresult = ValidationResultBuilder("id3").conflict(conflicting_term=HpTerm(hpo_id="HP:0012345", label="Something"),term=HpTerm(hpo_id="HP:0072345", label="Something else")).build()
        self.assertEqual("ERROR", vresult.error_level)
        self.assertEqual("CONFLICT", vresult.category)
        self.assertFalse(vresult.is_unfixable_error())


