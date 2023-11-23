import unittest
from src.pyphetools.creation import HpTerm
from src.pyphetools.validation import ValidationResult, ValidationResultBuilder



class TestValidationResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        term = HpTerm(hpo_id="HP:0000123", label="Fake label")
        cls._validation_result = ValidationResultBuilder(
            phenopacket_id="id1"
        ).redundant().set_term(term=term).build()

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