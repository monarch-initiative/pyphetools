
ACCEBTABLE_GENOMES = {"GRCh37", "GRCh38", "hg19", "hg38"}



# {'alt': 'C', 'chr': '16', 'pos': '1756403', 'ref': 'CG'}},

class Variant:
    """
    This encapsulates variant data that we retrieve from Variant Validator
    """
    def __init__(self, assembly, vcf_d) -> None:
        if not assembly in ACCEBTABLE_GENOMES:
            raise ValueError(f"Malformed assembly: \"{assembly}\"")
        self._assembly = assembly
        if not isinstance(vcf_d, dict):
            raise ValueError(f"vcf_d argument must be dictionary")
        self._chr = vcf_d.get('chr')
        self._position = int(vcf_d.get('pos'))
        self._ref = vcf_d.get('ref')
        self._alt = vcf_d.get('alt')
        
    @property
    def assembly(self):
        self._assembly
        
    @property
    def chr(self):
        self._chr
        
    @property
    def position(self):
        self._position
        
    @property
    def ref(self):
        self._ref
        
        
    @property
    def alt(self):
        self._alt
        
    def __str__(self):
        return f"{self._chr}:{self._position}{self._ref}-{self._alt}"
    
    def to_string(self):
        return self.__str__()