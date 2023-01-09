import phenopackets 

ACCEBTABLE_GENOMES = {"GRCh37", "GRCh38", "hg19", "hg38"}



# {'alt': 'C', 'chr': '16', 'pos': '1756403', 'ref': 'CG'}},

class Variant:
    """
    This encapsulates variant data that we retrieve from Variant Validator
    """
    def __init__(self, assembly, vcf_d, symbol=None, hgnc=None, hgvs=None, transcript=None, g_hgvs=None) -> None:
        if not assembly in ACCEBTABLE_GENOMES:
            raise ValueError(f"Malformed assembly: \"{assembly}\"")
        self._assembly = assembly
        if not isinstance(vcf_d, dict):
            raise ValueError(f"vcf_d argument must be dictionary")
        self._chr = vcf_d.get('chr')
        self._position = int(vcf_d.get('pos'))
        self._ref = vcf_d.get('ref')
        self._alt = vcf_d.get('alt')
        self._symbol = symbol
        self._hgnc_id = hgnc
        self._hgvs = hgvs
        self._transcript = transcript
        self._g_hgvs = g_hgvs
        self._genotype = None
        
    @property
    def assembly(self):
        return self._assembly
        
    @property
    def chr(self):
        return self._chr
        
    @property
    def position(self):
        return self._position
        
    @property
    def ref(self):
        return self._ref
        
    @property
    def alt(self):
        return self._alt
    
    @property
    def genotype(self):
        return self._genotype
    
    def set_genotype(self, gt):
        self._genotype = gt
        
        
    def __str__(self):
        return f"{self._chr}:{self._position}{self._ref}>{self._alt}"
    
    def to_string(self):
        return self.__str__()
    
    def to_ga4gh(self, acmg=None):
        """
        Transform this Variant object into a "variantInterpretation" message of the GA4GH Phenopacket schema
        """
        vdescriptor = phenopackets.VariationDescriptor()
        if self._hgnc_id is not None and self._symbol is not None:
            vdescriptor.gene_context.value_id = self._hgnc_id
            vdescriptor.gene_context.symbol = self._symbol
        hgvs_expression = phenopackets.Expression()
        if self._hgvs is not None:
            hgvs_expression.syntax = "hgvs.c"
            hgvs_expression.value = self._hgvs
            vdescriptor.expressions.append(hgvs_expression) 
        if self._g_hgvs is not None: 
            hgvs_expression.syntax = "hgvs.g"
            hgvs_expression.value = self._g_hgvs
            vdescriptor.expressions.append(hgvs_expression) 
        vdescriptor.molecule_context =  phenopackets.MoleculeContext.genomic
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
        vcf_record = phenopackets.VcfRecord()
        vcf_record.genome_assembly =  self._assembly
        vcf_record.chrom = self._chr
        vcf_record.pos = self._position
        vcf_record.ref = self._ref
        vcf_record.alt = self._alt
        vdescriptor.vcf_record.CopyFrom(vcf_record)
        vinterpretation.variation_descriptor.CopyFrom(vdescriptor)
        return vinterpretation
        