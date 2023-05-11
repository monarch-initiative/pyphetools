from .variant import Variant
from typing import List
from .variant_validator import VariantValidator
import pandas as pd

ACCEPTABLE_GENOTYPES = {"heterozygous", "homozygous", "hemizygous"}


class VariantColumnMapper:

    def __init__(self, assembly, transcript, column_name, default_genotype=None, genotype_column=None,
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
        self._variant_symbol_d = {}

    def map_cell(self, cell_contents, genotype_contents=None, delimiter=None) -> List[Variant]:
        if delimiter is None:
            delimiter = self._delimiter
        if delimiter is not None:
            items = [x.strip() for x in cell_contents.split(delimiter)]
        else:
            items = [cell_contents]
        results = []
        for item in items:
            if item in self._variant_symbol_d:
                variant_list = self._variant_symbol_d.get(item)
                for v in variant_list:
                    v.set_genotype(self._default_genotype)
                results.extend(variant_list)
            else:
                try:
                    variant = self._validator.encode_hgvs(item)
                    if genotype_contents is not None:
                        if 'hom' in genotype_contents.lower():
                            variant.set_genotype('homozygous')
                        elif 'het' in genotype_contents.lower():
                            variant.set_genotype('heterozygous')
                        elif 'hemi' in genotype_contents.lower():
                            variant.set_genotype('hemizygous')
                        elif self._default_genotype is not None:
                            variant.set_genotype(self._default_genotype)
                    else:
                        if self._default_genotype is not None:
                            variant.set_genotype(self._default_genotype)
                    results.append(variant)
                except Exception as exc:
                    print(f"Not able to get variant for {item}: {exc}")
        return results

    def preview_column(self, column) -> pd.DataFrame:
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for _, value in column.items():
            variants = self.map_cell(str(value))
            if len(variants) == 0:
                dlist.append({"variant": "n/a"})
            else:
                result_strings = []
                for v in variants:
                    result_strings.append(v.to_string())
                dlist.append({"variant": ": ".join(result_strings)})
        return pd.DataFrame(dlist)

    def get_column_name(self):
        return self._column_name

    def get_genotype_colname(self):
        return self._genotype_column

    def set_variant_symbol_dictionary(self, variant_sym_d):
        self._variant_symbol_d = variant_sym_d

    def _print_summary(self):
        """Dump some of the attributes of the object, for debugging
        """
        print("VariantColumnMapper")
        print(f"transcript: {self._transcript}")
        print(f"column_name: {self._column_name}")
        print(f"genotype_column: {self._genotype_column}")
        print(f"delimiter: {self._delimiter}")
        print(f"Size of _variant_symbol_d: {len(self._variant_symbol_d)}")

