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
        self.assertEquals(GENOME_ASSEMBLY, var.assembly)
        
    def test_position(self):
        self.assertEquals(1756403, self._variant.position)

