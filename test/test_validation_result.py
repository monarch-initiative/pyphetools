import unittest
from src.pyphetools.creation import HpTerm, AllelicRequirement
from src.pyphetools.validation import ValidationResultBuilder



class TestValidationResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        term = HpTerm(hpo_id="HP:0000123", label="Fake label")
        cls._validation_result = ValidationResultBuilder(
            phenopacket_id="id1"
        ).duplicate_term(redundant_term=term).build()

    def test_not_none(self):
        self.assertIsNotNone(self._validation_result)

    def test_phenopacket_id(self):
        self.assertEqual("id1", self._validation_result.id)

    def test_warning(self):
        """
        The function "redundant" in the builder should set the ErrorLevel to "WARNING"
        """
        self.assertTrue(self._validation_result.is_warning())

    def test_is_redundant(self):
        self.assertEqual("REDUNDANT", self._validation_result.category)

    def test_term(self):
        term = self._validation_result.term
        self.assertIsNotNone(term)
        self.assertEqual("HP:0000123", term.id)
        self.assertEqual("Fake label", term.label)

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

