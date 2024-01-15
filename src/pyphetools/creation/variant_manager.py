import os
import pickle
import pandas as pd
from typing import List, Dict
from collections import defaultdict
from .individual import Individual
from .variant_validator import VariantValidator
from .structural_variant import StructuralVariant

def get_pickle_filename(name):
    """
    provide standard filenaming convention. We pickle results from VariantValidator to avoid
    calling API multiple times in different runs. For instance, the pickled file of variants for
    the SCL4A1 cohort will be called "variant_validator_cache_SLC4A1.pickle"
    """
    return f"variant_validator_cache_{name}.pickle"

def load_variant_pickle(name):
    """
    Load the pickle file. If the file cannot be found, return None. If it is found, return the
     pickled object (which in our case will be a dictionary of Variant objects).
    """
    fname = get_pickle_filename(name)
    if not os.path.isfile(fname):
        return None
    # De-serialize the object from the file
    with open(fname, "rb") as f:
        loaded_object = pickle.load(f)
        return loaded_object

def write_variant_pickle(name, my_object):
    """
    Write a dictionary to pickled file
    :param my_object: In this application, this argument will be a dictionary of Variant objects).
    """
    fname = get_pickle_filename(name)
    with open(fname, "wb") as f:
        pickle.dump(my_object, f)



class VariantManager:
    """This class is designed to extract Variant objects from a pandas DataFrame that represents the input data.
    It will work out of the box for dataframes created by the CaseTemplateEncoder, and can be adapted to work
    with other datasets. The assumption is that there is one column per allele. For autosomal dominant, there would
    thus be one column. For recessive, there would be two columns. We do not try to automatically map non-HGVS (i.e.,
    chromosomal variants). Instead, we first map HGVS using VariantValidator, and then we return a Pandas DataFrame that
    shows the other variants. These can be use to create chromosomal deletions, duplications, and inversions. Finally,
    the class can be used to add variants to a list of Individual objects.

    :param df: DataFrame representing the input data
    :type df: pd.DataFrame
    :param individual_column_name: Name of the individual (patient) column
    :type individual_column_name: str
    :param cohort_name: a string that is used to name the pickle file that stores variant objects, usually the gene symbol
    :type cohort_name: str
    :param transcript: accession number and version of the transcript, e.g., "NM_000342.3"
    :type transcript: str
    :param allele_1_column_name: name of the column with alleles (#1)
    :type allele_1_column_name: str
    :param allele_2_column_name: name of the column with alleles (#2), optional
    :type allele_2_column_name: str
    :param gene_symbol: Symbol of affectged gene (only required if chromosomal variants need to be coded)
    :type gene_symbol: str
    :param gene_id: HGNC identifier of affectged gene (only required if chromosomal variants need to be coded)
    :type gene_id: str
    """

    def __init__(self,
                 df:pd.DataFrame,
                 individual_column_name:str,
                 cohort_name:str,
                 transcript:str,
                 allele_1_column_name:str,
                 allele_2_column_name:str=None,
                 gene_symbol:str=None,
                 gene_id:str=None
                 ):
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"The \"df\" argument must be a pandas DataFrame but was {type(df)}")
        if individual_column_name not in df.columns:
            raise ValueError(f"The \"individual_column_name\" argument must be a a column in df (a pandas DataFrame)")
        if allele_1_column_name not in df.columns:
            raise ValueError(f"The \"allele_1_column_name\" argument must be a a column in df (a pandas DataFrame)")
        if allele_2_column_name is not None and allele_2_column_name not in df.columns:
            raise ValueError(f"If not None, the \"allele_2_column_name\" argument must be a a column in df (a pandas DataFrame)")
        self._dataframe = df
        self._individual_column_name = individual_column_name
        self._cohort_name = cohort_name
        self._transcript = transcript
        self._allele_1_column_name = allele_1_column_name
        self._allele_2_column_name = allele_2_column_name
        self._gene_symbol = gene_symbol
        self._gene_id = gene_id
        self._var_d = {}
        self._unmapped_alleles = set()
        self._individual_to_alleles_d = defaultdict(list)
        self._create_variant_d()



    def _create_variant_d(self):
        """
        Creates a dictionary with all HGVS variants, and as a side effect creates a set with variants that
        are not HGVS and need to be mapped manually. This method has the following effects
        - self._var_d, a dictionary, is filled with key: HGVS strings, value: corresponding Variant objects
        - self._unmapped_alleles: set of all alleles that do not start eith "c." (non HGVS), that will need intervention by the user to map
        - self._individual_to_alleles_d: key individual ID, value-one or two element list of allele strings
        """
        v_d = load_variant_pickle(self._cohort_name)
        if v_d is None:
            self._var_d = {}
        else:
            self._var_d = v_d
        genome_assembly = "hg38"  # Nothing else is good enough, sorry hg19
        variant_set = set()  # we expect HGVS nomenclature. Everything else will be parsed as chromosomal
        vvalidator = VariantValidator(genome_build=genome_assembly, transcript=self._transcript)
        # The DataFrame has two header rows.
        # The second header row in effect is the first row of the DataFrame, so we drop it here.
        df = self._dataframe.iloc[1:]
        for _, row in df.iterrows():
            individual_id = row[self._individual_column_name]
            allele1 = row[self._allele_1_column_name]
            self._individual_to_alleles_d[individual_id].append(allele1)
            if allele1.startswith("c."):
                variant_set.add(allele1)
            else:
                self._unmapped_alleles.add(allele1)
            if self._allele_2_column_name is not None:
                allele2 = row[self._allele_2_column_name]
                self._individual_to_alleles_d[individual_id].append(allele2)
                if allele2.startswith("c."):
                    variant_set.add(allele2)
                else:
                    self._unmapped_alleles.add(allele2)
        for v in variant_set:
            if v in self._var_d:
                continue
            print(f"[INFO] encoding variant \"{v}\"")
            try:
                var = vvalidator.encode_hgvs(v)
            except Exception as e:
                print(f"[ERROR] Could not retrieve Variant Validator information for {v}: {str(e)}")
            self._var_d[v] = var
        write_variant_pickle(name=self._cohort_name, my_object=self._var_d)

    def code_as_chromosomal_deletion(self, allele_set):
        """
        Code as Structural variants - chromosomal deletion (to be added to self._var_d)
        :param allele_set: Set of alleles (strings) for coding as Structural variants (chromosomal deletion)
        """
        # first check that all of the alleles are in self._unmapped_alleles
        if not allele_set.issubset(self._unmapped_alleles):
            raise ValueError("[ERROR] We can only map alleles that were passed to the constructor - are you trying to map \"new\2 alleles?")
        if self._gene_id is None or self._gene_symbol is None:
            raise ValueError("[ERROR] We cannot use this method unless the gene ID (HGNC) and symbol were passed to the constructor")
        for allele in allele_set:
            var = StructuralVariant.chromosomal_deletion(cell_contents=allele, gene_symbol=self._gene_symbol, gene_id=self._gene_id)
            self._unmapped_alleles.remove(allele)
            self._var_d[allele] = var

    def code_as_chromosomal_duplication(self, allele_set):
        """
        Code as Structural variants - chromosomal duplication (to be added to self._var_d)
        :param allele_set: Set of alleles (strings) for coding as Structural variants (chromosomal duplication)
        """
        # first check that all of the alleles are in self._unmapped_alleles
        if not allele_set.issubset(self._unmapped_alleles):
            raise ValueError("[ERROR] We can only map alleles that were passed to the constructor - are you trying to map \"new\2 alleles?")
        if self._gene_id is None or self._gene_symbol is None:
            raise ValueError("[ERROR] We cannot use this method unless the gene ID (HGNC) and symbol were passed to the constructor")
        for allele in allele_set:
            var = StructuralVariant.chromosomal_duplication(cell_contents=allele, gene_symbol=self._gene_symbol, gene_id=self._gene_id)
            self._unmapped_alleles.remove(allele)
            self._var_d[allele] = var

    def code_as_chromosomal_inversion(self, allele_set) -> None:
        """
        Code as Structural variants - chromosomal inversion (to be added to self._var_d)
        :param allele_set: Set of alleles (strings) for coding as Structural variants (chromosomal inversion)
        """
        # first check that all of the alleles are in self._unmapped_alleles
        if not allele_set.issubset(self._unmapped_alleles):
            raise ValueError("[ERROR] We can only map alleles that were passed to the constructor - are you trying to map \"new\2 alleles?")
        if self._gene_id is None or self._gene_symbol is None:
            raise ValueError("[ERROR] We cannot use this method unless the gene ID (HGNC) and symbol were passed to the constructor")
        for allele in allele_set:
            var = StructuralVariant.chromosomal_inversion(cell_contents=allele, gene_symbol=self._gene_symbol, gene_id=self._gene_id)
            self._unmapped_alleles.remove(allele)
            self._var_d[allele] = var


    def to_summary(self) -> pd.DataFrame:
        """
        Create and return a DataFrame with current status of mapping efforts. The resulting dataframe can be used to
        check mapping and to retrieve the allele strings that could not be mapped (and therefore probably need to
        be mapped with one of the chromosomal methods)
        """
        dlist = []
        n_mapped = len(self._var_d)
        mapped_alleles = ", ".join(self._var_d.keys())
        d = {"status": "mapped", "count": n_mapped, "alleles": mapped_alleles}
        dlist.append(d)
        n_unmapped = len(self._unmapped_alleles)
        unmapped_alleles = ", ".join(self._unmapped_alleles)
        d = {"status": "unmapped", "count": n_unmapped, "alleles": unmapped_alleles}
        dlist.append(d)
        return pd.DataFrame(dlist)

    def add_variants_to_individuals(self, individual_list:List[Individual], hemizygous:bool=False):
        """
        Add Variant objects to individuals. Here, we use the map self._individual_to_alleles_d that
        relates the individual IDs to the allele strings in the original data, together with the
        map self._var_d, which relates the allele strings to Variant objects. If anything is missing, then
        we raise an Exception. Note currently this method cannot be used for X-dominant MOI.
        :param individual_list: list of Individuals to which we will add Variant objects
        :type individual_list: List[Individual]
        :param hemizygous: If True, this is an X-chromosomal gene and we assume hemizygous
        :type hemizygous: bool
        """
        if len(self._unmapped_alleles) > 0:
            raise ValueError(f"Need to map all allele strings before using this method but "
                            f"{len(self._unmapped_alleles)} were unmapped. Try variantManager.to_summary()")
        for i in individual_list:
            if i.id not in self._individual_to_alleles_d:
                raise ValueError(f"Did not find {i.id} in our dictionary of individuals")
            vlist = self._individual_to_alleles_d.get(i.id)
            if len(vlist) == 1:
                # assume monoallelic
                v = vlist[0]
                if v not in self._var_d:
                    raise ValueError(f"Could not find {v} in variant dictionary")
                var = self._var_d.get(v)
                if hemizygous:
                    var.set_hemizygous()
                else:
                    var.set_heterozygous()
                i.add_variant(var)
            elif len(vlist) == 2:
                if hemizygous:
                    raise ValueError("hemizygous argument set to True in present of two alleles")
                # assume biallelic
                v1 = vlist[0]
                v2 = vlist[1]
                if v1 not in self._var_d:
                    raise ValueError(f"Could not find {v1} in variant dictionary")
                if v2 not in self._var_d:
                    raise ValueError(f"Could not find {v2} in variant dictionary")
                if v1 == v2:
                    var = self._var_d.get(v1)
                    var.set_homozygous()
                    i.add_variant(var)
                else:
                    var1 = self._var_d.get(v1)
                    var1.set_heterozygous()
                    i.add_variant(var1)
                    var2 = self._var_d.get(v2)
                    var2.set_heterozygous()
                    i.add_variant(var2)





