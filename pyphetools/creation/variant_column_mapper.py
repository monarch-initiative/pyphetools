from collections import defaultdict
import pandas as pd
from typing import List
from .hgvs_variant import Variant
from .variant_validator import VariantValidator
from .variant import Variant


ACCEPTABLE_GENOTYPES = {"heterozygous", "homozygous", "hemizygous"}


class VariantColumnMapper:

    def __init__(self, 
                 assembly, 
                 transcript, 
                 column_name, 
                 default_genotype=None, 
                 genotype_column=None,
                 non_hgvs_variant_map=defaultdict(),
                 delimiter=None) -> None:
        """Column mapper for HGVS expressions containing the variants identified in individuals

        Args:
            assembly (str): The genome assembly
            transcript (str): The default transcript to use to map the HGVS expressions
            default_genotype (str): The genotype of the variants (unless otherwise specified)
            genotype_column (str): Label of the column that contains the genotype (if available)
            delimiter (str): symbol used to separate variants if more than one variant is provided.
        """
        if default_genotype is not None and default_genotype not in ACCEPTABLE_GENOTYPES:
            raise ValueError(f"Did not recognize default genotype {default_genotype}")
        self._default_genotype = default_genotype
        if transcript is None or len(transcript) < 3:
            raise ValueError(f"Invalid transcript: \"{transcript}\"")
        self._transcript = transcript
        self._validator = VariantValidator(genome_build=assembly, transcript=transcript)
        self._column_name = column_name
        self._genotype_column = genotype_column
        self._delimiter = delimiter
        self._non_hgvs_variant_map = non_hgvs_variant_map

    def map_cell(self, cell_contents, genotype_contents=None, delimiter=None) -> List[Variant]:
        if delimiter is None:
            delimiter = self._delimiter
        if delimiter is not None:
            items = [x.strip() for x in cell_contents.split(delimiter)]
        else:
            items = [cell_contents]
        variant_interpretation_list = []
        for item in items:
            if item in self._non_hgvs_variant_map:
                variant: Variant = self._non_hgvs_variant_map.get(item)
                interpretation = variant.to_ga4gh_variant_interpretation()
                variant_interpretation_list.append(interpretation)
            else:
                try:
                    variant = self._validator.encode_hgvs(item)
                    if genotype_contents is not None:
                        if 'hom' in genotype_contents.lower():
                            variant.set_homozygous()
                        elif 'het' in genotype_contents.lower():
                            variant.set_heterozygous()
                        elif 'hemi' in genotype_contents.lower():
                            variant.set_hemizygous()
                        else:
                            print(f"Did not recognize genotype {genotype_contents}")
                    elif self._default_genotype is not None:
                        def_gt = self._default_genotype
                        if 'hom' in def_gt:
                            variant.set_homozygous()
                        elif 'het' in def_gt:
                            variant.set_heterozygous()
                        elif 'hemi' in def_gt:
                            variant.set_hemizygous()
                    variant_interpretation_list.append(variant.to_ga4gh_variant_interpretation())
                except Exception as exc:
                    print(f"Not able to get variant for {item}: {exc}")
        return variant_interpretation_list
    
    
    def variant_interpretation_to_string(self, vinterpretation):
        # first check for HGVS
        if vinterpretation.variation_descriptor is None:
            raise ValueError("VariantInterpretation must have VariationDescriptor element")
        vdescriptor = vinterpretation.variation_descriptor
        for exprss in vdescriptor.expressions:
            if exprss.syntax == "hgvs.c":
                return exprss.value
        # then check for a description
        if vdescriptor.label is not None:
            return vdescriptor.label
        else:
            return vinterpretation.id


    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            variant_interpretation_list = self.map_cell(str(value))
            if len(variant_interpretation_list) == 0:
                dlist.append({"variant": "n/a"})
            else:
                result_strings = []
                for v in variant_interpretation_list:
                    result_strings.append(self.variant_interpretation_to_string(v))
                dlist.append({"variant": ": ".join(result_strings)})
        return pd.DataFrame(dlist)

    def get_column_name(self):
        return self._column_name

    def get_genotype_colname(self):
        return self._genotype_column

    def _print_summary(self):
        """Dump some of the attributes of the object, for debugging
        """
        print("VariantColumnMapper")
        print(f"transcript: {self._transcript}")
        print(f"column_name: {self._column_name}")
        print(f"genotype_column: {self._genotype_column}")
        print(f"delimiter: {self._delimiter}")
        print(f"Size of _variant_symbol_d: {len(self._variant_symbol_d)}")

