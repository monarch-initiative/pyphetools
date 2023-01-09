import unittest
import json
from pyphetools.creation import Variant

# The following dictionary has the same structure as a subelement of the response from Variant Validator
VCF_DICTIONARY =  {'alt': 'C', 'chr': '16', 'pos': '1756403', 'ref': 'CG'}
GENOME_ASSEMBLY = 'hg38'
transcript = 'NM_015133.4'
symbol = 'MAPK8IP3'
hgvs = 'NM_015133.4:c.111C>G'
hgnc_id = 'HGNC:6884'
g_hgvs = 'NC_000016.10:g.1706450C>G'

class TestVariantValidator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls._variant = Variant(assembly=GENOME_ASSEMBLY, vcf_d=VCF_DICTIONARY, symbol=symbol, 
                               hgnc=hgnc_id, hgvs=hgvs, transcript=transcript, g_hgvs=g_hgvs)
        
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
        
    def test_to_ga4gh(self):
        variant_descriptor = self._variant.to_ga4gh()
        self.assertIsNotNone(variant_descriptor)

