import unittest
import json
from pyphetools import Variant

# The following dictionary has the same structure as a subelement of the response from Variant Validator
VCF_DICTIONARY =  {'alt': 'C', 'chr': '16', 'pos': '1756403', 'ref': 'CG'}
GENOME_ASSEMBLY = 'hg38'

class TestVariantValidator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls._variant = Variant(assembly=GENOME_ASSEMBLY, vcf_d=VCF_DICTIONARY)
        
    def test_obect_created(self):
        self.assertIsNotNone(self._variant)
        
    def test_assembly(self):
        var = self._variant
        self.assertEqual(GENOME_ASSEMBLY, var.assembly)
        
    def test_chr(self):
        var = self._variant
        self.assertEqual('16', var.chr)
        
    def test_position(self):
        self.assertEqual(1756403, self._variant.position)
        
    def test_ref(self):
        var = self._variant
        self.assertEqual('CG', var.ref)
        
    def test_alt(self):
        var = self._variant
        self.assertEqual('C', var.alt)

