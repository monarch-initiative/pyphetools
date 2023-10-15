import pandas as pd
from typing import List, Dict

from .variant import Variant

ACCEPTABLE_GENOTYPES = {"heterozygous", "homozygous", "hemizygous"}


class VariantColumnMapper:
    """Column mapper for the variants identified in individuals

    To use this mapper, first create a dictionary with all variants in the cohort using the
    VariantValidator (for HGVS) and the StructuralVariant classes. The key to the variant is
    the cell contents of the column with variant information in the original table. The Values
    are the Variant objects (implemented as HgvsVariant or StructuralVariant). This mapper will
    split cells that contain multiple variants if needed and also will add genotype information.

    :param variant_d: Dictionary with all variants found in the column
    :type variant_d: Dict[str,Variant]
    :param variant_column_name: name of the variant column in the original table
    :type variant_column_name: str
    :param genotype_column_name: name of the genotype column in the original table, optional
    :type genotype_column_name: str
    :param delimiter: symbol used to separate variants if more than one variant is provided, optional
    :type delimiter: str
    """
    def __init__(self,
                 variant_d,
                 variant_column_name,
                 genotype_column_name=None,
                 default_genotype=None,
                 delimiter=None) -> None:

        if default_genotype is not None and default_genotype not in ACCEPTABLE_GENOTYPES:
            raise ValueError(f"Did not recognize default genotype {default_genotype}")
        if not isinstance(variant_d, dict):
            raise ValueError(f"Argument variant_d must be a dictionary but was {type(variant_d)}")
        self._variant_d = variant_d
        self._default_genotype = default_genotype
        self._variant_column_name = variant_column_name
        self._genotype_column_name = genotype_column_name
        self._delimiter = delimiter


    def _get_genotype(self, genotype_contents):
        """
        Get a genotype string

        get the genotype from the argument (which comes from the genotype column if available) or from the
        default genotype.
        :returns: one of "heterozygous", "homozygous", "hemizygous", None
        """
        if genotype_contents is not None and genotype_contents.lower() in ACCEPTABLE_GENOTYPES:
            return genotype_contents.lower()
        else:
            return self._default_genotype


    def map_cell(self, cell_contents, genotype_contents=None, delimiter=None) -> List[Variant]:
        """
        Map the contents of a variant cell (and optionally a genotype cell).

        If the delimiter is not None, search for the delimiter and split the cell into two variants
        :param cell_contents: contents of the original table cell representing the variant string
        :type cell_contents: str
        :param genotype_contents: contents of the original table cell representing the genotype (allelic status), optional
        :type genotype_contents: str
        :param delimiter: string or character that splits the cell contents into multiple entries, e.g., ";", optional
        :type delimiter: str
        """
        if delimiter is None:
            delimiter = self._delimiter
        if delimiter is not None:
            items = [x.strip() for x in cell_contents.split(delimiter)]
        else:
            items = [cell_contents]
        variant_interpretation_list = []
        for item in items:
            if item in self._variant_d:
                variant: Variant = self._variant_d.get(item)
                gt = self._get_genotype(genotype_contents)
                if gt is not None:
                    variant.set_genotype(gt)
                interpretation = variant.to_ga4gh_variant_interpretation()
                variant_interpretation_list.append(interpretation)
            else:
                raise ValueError(f"Did not recognize variant string \"{item}\"")

        return variant_interpretation_list



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
                    result_strings.append(v.__str__())
                dlist.append({"variant": ": ".join(result_strings)})
        return pd.DataFrame(dlist)

    def get_variant_column_name(self):
        return self._variant_column_name

    def get_genotype_colname(self):
        return self._genotype_column_name


