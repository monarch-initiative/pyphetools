from google.protobuf.json_format import Parse
import json
import os
import phenopackets
from .phenopacket_validator import PhenopacketValidator
from .validation_result import ValidationResult
from typing import List


class ContentValidator(PhenopacketValidator):
    def __init__(self, min_var:int, min_hpo:int, min_allele:int=None) -> None:
        self._min_var = min_var
        self._min_hpo = min_hpo
        self._min_allele = min_allele
        
        
    def validate_phenopacket(self, phenopacket) -> List[ValidationResult]:
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
        validation_results = []
        n_pf = len(phpacket.phenotypic_features)
        if phpacket.interpretations is None:
            n_var = 0
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
        valid = True
        if n_pf < self._min_hpo:
            msg = f"Minimum HPO terms required {self._min_hpo} but only {n_pf} found"
            validation_results.append(ValidationResult.error(phenopacket_id=pp_id, message=msg))
        if n_var < self._min_var:
            msg = f"Minimum variants required {self._min_var} but only {n_var} found"
            validation_results.append(ValidationResult.error(phenopacket_id=pp_id, message=msg))
        if self._min_allele is not None and n_alleles < self._min_allele:
            msg = f"Minimum alleles required {self._min_allele} but only {n_alleles} found"
            validation_results.append(ValidationResult.error(phenopacket_id=pp_id, message=msg))
        return validation_results
    
    def validate_phenopacket_list(self, phenopacket_list) -> List[ValidationResult]:
        """phenopacket_list can be a list of phenopacket objects or paths to JSON files

        Args:
            phenopacket_list (_type_): _description_

        Returns:
            List[ValidationResult]: _description_
        """
        validation_results = []
        for pp in phenopacket_list:
            validation_results.extend(self.validate_phenopacket(pp))
        return validation_results
 

                            
                