from .variant import Variant
from typing import List
from .variant_validator import VariantValidator
import pandas as pd

ACCEPTABLE_GENOTYPES = {"heterozygous", "homozygous", "hemizygous"}



class VariantColumnMapper:
    
    def __init__(self, assembly, transcript, column_name, genotype=None) -> None:
        """
        genotype -- the 'default' for all variants in this column
        """
        if genotype is not None and genotype not in ACCEPTABLE_GENOTYPES:
            raise ValueError(f"Did not recognize default genotype {genotype}")
        self._genotype = genotype
        if transcript is None or len(transcript) < 3:
            raise ValueError(f"Invalid transcript: \"{transcript}\"")
        self._transcript = transcript
        self._validator = VariantValidator(genome_build=assembly, transcript=transcript)
        self._column_name = column_name
        
    def map_cell(self, cell_contents, delimiter=None) -> List[Variant]:
        if delimiter is not None:
            items = [x.strip() for x in cell_contents.split(delimiter)]
        else:
            items = [cell_contents.strip()]
        results = []
        for item in items:
            try:
                variant = self._validator.encode_hgvs(item)
                if self._genotype is not None:
                    variant.set_genotype(self._genotype)
                results.append(variant)
            except Exception as exc:
                print(f"Not able to get variant for {item}: {exc}")
        return results
    
    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            variants  = self.map_cell(str(value))
            if len(variants) == 0:
                dlist.append({"variant": "n/a"})
            else:
                result_strings = []
                for v in  variants:
                    result_strings.append(v.to_string()) 
                dlist.append({"variant": ": ".join(result_strings)})
        return pd.DataFrame(dlist)  
    
    def get_column_name(self):
        return self._column_name
