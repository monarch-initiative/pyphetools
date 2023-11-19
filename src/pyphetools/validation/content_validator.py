import json
import os
from typing import List, Optional

import phenopackets
from google.protobuf.json_format import Parse

from .phenopacket_validator import PhenopacketValidator
from .validation_result import ValidationResult, ValidationResultBuilder
from ..creation.allelic_requirement import AllelicRequirement
from ..creation.individual import Individual


class ContentValidator(PhenopacketValidator):
    """
    Validate a list of phenopackets as to whether they have a minunum number of phenotypic features and alleles

    The following example shows how to use this class to assess whether each phenopacket in the directory called "phenopackets" contains at least one variant and at least three HPO terms.

        from pyphetools.visualization import PhenopacketIngestor
        from pyphetools.validation import ContentValidator
        ingestor = PhenopacketIngestor(indir="phenopackets")
        ppkt_d = ingestor.get_phenopacket_dictionary()
        ppkt_list = list(ppkt_d.values())
        validator = ContentValidator(min_var=1, min_hpo=3)
        errors = validator.validate_phenopacket_list(ppkt_list)
        print(f"{len(errors)} errors were identified")

    Note that this class does not test for all errors. Use phenopacket-tools to check for redundant or conflicting
    annotations.

    :param min_hpo: minimum number of phenotypic features (HP terms) for this phenopacket to be considered valid
    :type min_hpo: int
    :param allelic_requirement: used to check number of alleles and variants
    :type allelic_requirement: AllelicRequirement
    """
    def __init__(self, min_hpo: int, allelic_requirement: AllelicRequirement = None) -> None:
        super().__init__()
        self._min_hpo = min_hpo
        self._allelic_requirement = allelic_requirement


    def validate_individual(self, individual:Individual) -> List[ValidationResult]:
        """
        check a single Individual as to whether there are sufficient HPO terms and alleles/variants
        :returns: a potential empty list of validations
        :rtype: List[ValidationResult]
        """
        n_pf = len(individual.hpo_terms)
        n_var = 0
        n_alleles = 0
        pp_id = individual.get_phenopacket_id()
        for variant_interpretation in individual.interpretation_list:
            n_var += 1
            if variant_interpretation.variation_descriptor is not None:
                vdesc =  variant_interpretation.variation_descriptor
                if vdesc.allelic_state is not None:
                    gtype = vdesc.allelic_state
                    if gtype.label == "heterozygous": # "GENO:0000135"
                        n_alleles += 1
                    elif gtype.label == "homozygous": # "GENO:0000136"
                        n_alleles += 2
                    elif gtype.label == "hemizygous": # "GENO:0000134"
                        n_alleles += 1
        return self._validate(pp_id=pp_id, n_hpo=n_pf, n_var=n_var, n_alleles=n_alleles)



    def validate_phenopacket(self, phenopacket) -> List[ValidationResult]:
        """
        check a single phenopacket as to whether there are sufficient HPO terms and alleles/variants
        :returns: a potential empty list of validations
        :rtype: List[ValidationResult]
        """
        if isinstance(phenopacket, str):
            # the user passed a file
            if not os.path.isfile(phenopacket):
                raise FileNotFoundError(f"Could not find phenopacket file at '{phenopacket}'")
            with open(phenopacket) as f:
                data = f.read()
                jsondata = json.loads(data)
                phpacket = Parse(json.dumps(jsondata), phenopackets.Phenopacket())
        elif isinstance(phenopacket, phenopackets.Phenopacket):
            phpacket = phenopacket
        else:
            raise ValueError(f"phenopacket argument must be file path or GA4GH Phenopacket \
                object but was {type(phenopacket)}")
        pp_id = phpacket.id
        n_pf = len(phpacket.phenotypic_features)
        if phpacket.interpretations is None:
            n_var = 0
            n_alleles = 0
        else:
            n_var = 0
            n_alleles = 0
            for interpretation in phpacket.interpretations:
                if interpretation.diagnosis is not None:
                    dx = interpretation.diagnosis
                    for genomic_interpretation in dx.genomic_interpretations:
                        n_var += 1
                        vint = genomic_interpretation.variant_interpretation
                        if vint.variation_descriptor is not None:
                            vdesc =   vint.variation_descriptor
                            if vdesc.allelic_state is not None:
                                gtype = vdesc.allelic_state
                                if gtype.label == "heterozygous": # "GENO:0000135"
                                    n_alleles += 1
                                elif gtype.label == "homozygous": # "GENO:0000136"
                                    n_alleles += 2
                                elif gtype.label == "hemizygous": # "GENO:0000134"
                                    n_alleles += 1
        return self._validate(pp_id=pp_id, n_hpo=n_pf, n_var=n_var, n_alleles=n_alleles)



    def _validate(self, pp_id:str, n_hpo:int, n_var:int=None, n_alleles:int=None):
        """
        private method called by validate_individual or validate_phenopacket.
        :param pp_id: phenopacket identifier
        :type pp_id: str
        :param n_hpo: Number of HPO terms
        :type n_hpo: int
        :param n_var: Number of variants found
        :type n_var: Optional[int]
        :param n_alleles: Number of alleles found
        :type n_alleles: Optional[int]
        """
        validation_results = []
        if n_hpo < self._min_hpo:
            msg = f"Minimum HPO terms required {self._min_hpo} but only {n_hpo} found"
            validation_results.append(ValidationResult.error(phenopacket_id=pp_id, message=msg))
        if self._allelic_requirement is None:
            return validation_results
        if self._allelic_requirement == AllelicRequirement.MONO_ALLELIC:
            if n_var != 1:
                msg = f"Expected one variant for monoallelic but got {n_var} variants"
                val_result = ValidationResultBuilder(phenopacket_id=pp_id).error().incorrect_variant_count().set_message(msg=msg).build()
                validation_results.append(val_result)
            if n_alleles != 1:
                msg = f"Expected one allele for monoallelic but got {n_alleles} alleles"
                val_result = ValidationResultBuilder(phenopacket_id=pp_id).error().incorrect_allele_count().set_message(msg=msg).build()
                validation_results.append(val_result)
        elif self._allelic_requirement == AllelicRequirement.BI_ALLELIC:
            if n_var < 1 or n_var > 2:
                msg = f"Expected one or two variant for biallelic but got {n_var} variants"
                val_result = ValidationResultBuilder(phenopacket_id=pp_id).error().incorrect_variant_count().set_message(msg=msg).build()
                validation_results.append(val_result)
            if n_alleles != 2:
                msg = f"Expected two alleles for biallelic but got {n_alleles} alleles"
                val_result = ValidationResultBuilder(phenopacket_id=pp_id).error().incorrect_allele_count().set_message(msg=msg).build()
                validation_results.append(val_result)
        return validation_results






