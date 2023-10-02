import unittest
import os
import phenopackets as PPkt
from src.pyphetools.visualization import SimpleVariant
from src.pyphetools.creation import StructuralVariant

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')

class TestHpoParser(unittest.TestCase):


    def test_structural_variant_display(self):
        eri1_id = "HGNC:23994"
        eri1_sumbol = "ERI1"
        sv = StructuralVariant.chromosomal_deletion(cell_contents="g.8783887_9068578del", gene_id=eri1_id, gene_symbol=eri1_sumbol)
        variant_interpretation = sv.to_ga4gh_variant_interpretation()
        genomic_interpretation = PPkt.GenomicInterpretation()
        genomic_interpretation.subject_or_biosample_id = "some.id"
        # by assumption, variants passed to this package are all causative
        genomic_interpretation.interpretation_status = PPkt.GenomicInterpretation.InterpretationStatus.CAUSATIVE
        genomic_interpretation.variant_interpretation.CopyFrom(variant_interpretation)
        simpleVar = SimpleVariant(genomic_interpretation)
        self.assertEqual("g.8783887_9068578del: chromosomal_deletion (SO:1000029)", simpleVar.get_display())