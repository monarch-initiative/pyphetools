import phenopackets
from google.protobuf.json_format import MessageToJson

NA_STRING = "n/a"


class SimpleVariant:
    """Representation of a variant to facilitate display

        This class flattens information about variants from an
        GenomicInterpretation obtained from a phenopacket

        :param ginterpretation: A GenomicInterpretation object representing one variant and its interpretation
        :type ginterpretation: phenopackets.schema.v2.phenopackets_pb2.GenomicInterpretation
        """
    def __init__(self, ginterpretation) -> None:
        
        if str(type(ginterpretation)) != "<class 'phenopackets.schema.v2.core.interpretation_pb2.GenomicInterpretation'>":
            raise ValueError(f"interpretation argument must be GA4GH Phenopacket GenomicInterpretation but was {type(ginterpretation)}")
        self._status = str(ginterpretation.interpretation_status)
        vinterpretation = ginterpretation.variant_interpretation
        if vinterpretation.variation_descriptor is  None:
            raise ValueError("variation_descriptor was None")
        vdescript = vinterpretation.variation_descriptor
        if vdescript.gene_context is not None:
            self._gene_id = vdescript.gene_context.value_id
            self._gene_symbol = vdescript.gene_context.symbol
        else:
            self._gene_id = NA_STRING
            self._gene_symbol = NA_STRING
        self._hgvs = NA_STRING
        if vdescript.expressions is not None and len(vdescript.expressions) > 0:
            for exprsn in vdescript.expressions:
                if exprsn.syntax == "hgvs.c":
                    self._hgvs = exprsn.value       
        if vdescript.vcf_record is not None and len(vdescript.vcf_record.chrom) > 0:
            vcf = vdescript.vcf_record
            self._genome_ass = vcf.genome_assembly
            self._chrom = vcf.chrom
            self._pos = int(vcf.pos)
            self._ref = vcf.ref
            self._alt = vcf.alt
        else:
            self._genome_ass = NA_STRING
            self._chrom = NA_STRING
            self._pos = -1
            self._ref = NA_STRING
            self._alt = NA_STRING
        if vdescript.allelic_state is not None:
            allelic = vdescript.allelic_state
            self._genotype_id = allelic.id
            self._genotype_label = allelic.label
        else:
            self._genotype_id = NA_STRING
            self._genotype_label = NA_STRING
        if vdescript.structural_type is not None:
            so_id = vdescript.structural_type.id
            so_label = vdescript.structural_type.label
            self._structural = f"{so_label} ({so_id})"
        else:
            self._structural = None
        self._description_label = vdescript.label

    @property
    def status(self):
        return self._status

    @property
    def gene_id(self):
        return self._gene_id

    @property
    def gene_symbol(self):
        return self._gene_symbol
    
    @property
    def hgvs(self):
        return self._hgvs

    @property
    def genome_assembly(self):
        return self._genome_ass
    
    @property
    def chrom(self):
        return self._chrom

    @property
    def position(self):
        return self._pos

    @property
    def ref(self):
        return self._ref

    @property
    def alt(self):
        return self._alt

    @property
    def genotype_id(self):
        """
       :returns: the Sequence Ontology id for this variant, optional
       :rtype: str
       """
        return self._genotype_id

    @property
    def genotype_label(self):
        return self._genotype_label

    def has_vcf(self):
        """
        :returns: True if there is VCF data for this variant, otherwise False
        """
        return self._chrom != NA_STRING

    def has_genotype(self):
        """
        :returns: True if there is a genotype for this variant, otherwise False
        """
        return self._genotype_id != NA_STRING
    
    
    def get_display(self):
        """
        :returns: a string representing a human-readable representation of the variant
        """
        if self.has_genotype():
            genotype = "(" + self._genotype_label + ")"
        else:
            genotype = ""
        if self._hgvs != NA_STRING:
            return self._hgvs + " " + genotype
        if self.has_vcf():
            vcf_str = f"{self.chrom}:{self.position}{self.ref}>{self.alt} {genotype}"
            return vcf_str
        elif self._structural is not None:
            # try to return information about a structural variant.
            var_str = f"{self._description_label}: {self._structural}"
            return var_str
        else:
            return "n/a"
