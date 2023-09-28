import requests
from .hgvs_variant import HgvsVariant


URL_SCHEME = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/%s/%s%%3A%s/%s?content-type=application%%2Fjson"
ACCEPTABLE_GENOMES = {"GRCh37", "GRCh38", "hg19", "hg38"}



class VariantValidator:
    """
    Check and Encode HGVS string

    The default mRNA transcript for the HGVS strings should be added in the constructor byt can be overridden in the
    encode_hgvs method.

    :param genome_build: The genome assembly, one of "GRCh37", "GRCh38", "hg19", "hg38"
    :type genome_build: str
    :param transcript: An mRNA transcript that is the reference for the HGVS string, opt
    :type transcript: str
    """
    
    def __init__(self, genome_build, transcript=None):
        """
        Constructor
        """
        if genome_build not in ACCEPTABLE_GENOMES:
            raise ValueError(f"genome_build \"{genome_build}\" not recognized")
        self._genome_assembly = genome_build
        self._transcript = transcript
        
    def encode_hgvs(self, hgvs, custom_transcript=None):
        """
        Encode an HGVS string as a pyphetools Variant object

        :param hgvs: Human Genome Variation Society (HGVS) representation of a variant, e.g., c.36613706dup
        :type hgvs: str
        :param custom_transcript: a transcript (e.g., NM_001848.2), if different from the default transcript, optional
        :type custom_transcript: str
        :returns: pyphetools Variant object
        :rtype: HgvsVariant
        """
        if custom_transcript is not None:
            transcript = custom_transcript
        elif self._transcript is not None:
            transcript = self._transcript
        else:
            raise ValueError("Cannot run variant validator without transcript")
        api_url = URL_SCHEME % (self._genome_assembly, transcript, hgvs, transcript)
        #f"https://rest.variantvalidator.org/VariantValidator/variantvalidator/{self._genome_assembly}/{transcript}%3A{hgvs}/{transcript}"
        #
        print(api_url)
        response = requests.get(api_url)
        # We expect to get a dictionary with three keys. The first is the name of the variant, e.g., ACC:HGVS, then we
        # get flag and metadata
        vv_dict = response.json() 
        if 'flag' in vv_dict:
            if vv_dict['flag'] != 'gene_variant':
                flag = vv_dict['flag']
                raise ValueError(f"Expecting to get a gene_variant from Variant Validator but got {flag}")
        # This is the easiest way to get the variant key, which may contain difficult characters
        variant_key = [k for k in vv_dict.keys() if k not in {'flag', 'metadata'}][0]
        var = vv_dict[variant_key]
        hgnc = None
        if 'gene_ids' in var and 'hgnc_id' in var['gene_ids']:
            hgnc = var['gene_ids']['hgnc_id']
        symbol = None
        if 'gene_symbol' in var:
            symbol = var['gene_symbol']
        assemblies = var['primary_assembly_loci']
        if not self._genome_assembly in assemblies:
            raise ValueError(f"Could not identified {self._genome_assembly} in Variant Validator response")
        assembly = assemblies[self._genome_assembly]
        hgvs_transcript_var = var.get('hgvs_transcript_variant', None)
        genomic_hgvs = assembly.get('hgvs_genomic_description', None)
        reference_sequence_records = var.get('reference_sequence_records', None)
        if reference_sequence_records is not None:
            transcript = reference_sequence_records['transcript']
            if transcript.startswith('https://www.ncbi.nlm.nih.gov/nuccore/'):
                transcript = transcript[37:]
        else:
            transcript = None
       
        # 'vcf': {'alt': 'C', 'chr': '16', 'pos': '1756403', 'ref': 'CG'}},
        if not 'vcf' in assembly:
            raise ValueError(f"Could not identify vcf element in Variant Validator genome assembly response")
        return HgvsVariant(assembly=self._genome_assembly, vcf_d=assembly['vcf'], symbol=symbol, 
                       hgnc=hgnc, transcript=transcript, hgvs=hgvs_transcript_var, g_hgvs=genomic_hgvs)
  

        