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
                transcript:str,
                gene_symbol:str,
                allele_1_column_name:str,
                allele_2_column_name:str=None,
                gene_id:str=None,
                overwrite:bool=False
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
        self._transcript = transcript
        self._allele_1_column_name = allele_1_column_name
        self._allele_2_column_name = allele_2_column_name
        self._gene_symbol = gene_symbol
        self._gene_id = gene_id
        self._var_d = {}
        self._unmapped_alleles = set()
        self._individual_to_alleles_d = defaultdict(list)
        if "PMID" in df.columns:
            self._pmid_column_name = "PMID"
        else:
            self._pmid_column_name = None
        self._create_variant_d(overwrite)


    def _format_pmid_id(self, identifier, pmid):
        if pmid is not None:
            return f"{pmid}_{identifier}"
        else:
            return identifier

    def _get_identifier_with_pmid(self, row:pd.Series):
        """Get an identifier such as PMID_33087723_A2 for a daa row with PMID:33087723 and identifier within that publication A2

        Identifiers such as P1 are commonly used and there is a risk of a clash with collections of phenopackets from various papers.
        Therefore, we use an identifier such as PMID_33087723_A2 if we can find a PMID
        """
        individual_id = row[self._individual_column_name]
        individual_id = str(individual_id) # prevent automatic conversion into int for patient id 1, 2, 3 etc
        if self._pmid_column_name is not None:
            return self._format_pmid_id(identifier=individual_id, pmid=row[self._pmid_column_name])
        else:
            return individual_id

    def _create_variant_d(self, overwrite):
        """
        Creates a dictionary with all HGVS variants, and as a side effect creates a set with variants that
        are not HGVS and need to be mapped manually. This method has the following effects
        - self._var_d, a dictionary, is filled with key: HGVS strings, value: corresponding Variant objects
        - self._unmapped_alleles: set of all alleles that do not start eith "c." (non HGVS), that will need intervention by the user to map
        - self._individual_to_alleles_d: key individual ID, value-one or two element list of allele strings
        """
        if overwrite:
            v_d = {}
        else:
            v_d = load_variant_pickle(self._gene_symbol)
        if v_d is None:
            self._var_d = {}
        else:
            self._var_d = v_d
        genome_assembly = "hg38"  # Nothing else is good enough, sorry hg19
        variant_set = set()  # we expect HGVS nomenclature. Everything else will be parsed as chromosomal
        vvalidator = VariantValidator(genome_build=genome_assembly, transcript=self._transcript)
        # The DataFrame has two header rows.
        # For CaseTemplateEncoder, the second header row in effect is the first row of the DataFrame, so we drop it here.
        # For CaseTemplateEncoder, the second row will contain "str" in the second row of the PMID column
        # For other encoders, there may not be a "PMID" column, and if so it will not contain "CURIE" in the second row
        if "PMID" in self._dataframe.columns and self._dataframe.iloc[0]["PMID"] == "CURIE":
            df = self._dataframe.iloc[1:]
        else:
            df = self._dataframe
        for _, row in df.iterrows():
            individual_id = self._get_identifier_with_pmid(row=row)
            allele1 = row[self._allele_1_column_name]
            if allele1.startswith(" ") or allele1.endswith(" "):
                raise ValueError(f"Malformed allele_1 description that starts/ends with whitespace: \"{allele1}\".")
            self._individual_to_alleles_d[individual_id].append(allele1)
            if allele1.startswith("c."):
                variant_set.add(allele1)
            else:
                self._unmapped_alleles.add(allele1)
            if self._allele_2_column_name is not None:
                allele2 = row[self._allele_2_column_name]
                if allele2 is None:
                    continue
                if allele2 == "na" or allele2 == "n/a":
                    continue
                self._individual_to_alleles_d[individual_id].append(allele2)
                if allele2.startswith(" ") or allele2.endswith(" "):
                    raise ValueError(f"Malformed allele_2 description that starts/ends with whitespace: \"{allele2}\".")
                if allele2.startswith("c."):
                    variant_set.add(allele2)
                else:
                    self._unmapped_alleles.add(allele2)
        for v in variant_set:
            if v in self._var_d:
                continue
            if v == "na" or v == "n/a":
                continue
            print(f"[INFO] encoding variant \"{v}\"")
            try:
                var = vvalidator.encode_hgvs(v)
                self._var_d[v] = var
            except Exception as e:
                print(f"[ERROR] Could not retrieve Variant Validator information for {v}: {str(e)}")
                self._unmapped_alleles.add(v) # This allows us to use the chromosomal mappers.
        write_variant_pickle(name=self._gene_symbol, my_object=self._var_d)

    def code_as_chromosomal_deletion(self, allele_set):
        """
        Code as Structural variants - chromosomal deletion (to be added to self._var_d)
        :param allele_set: Set of alleles (strings) for coding as Structural variants (chromosomal deletion)
        """
        # first check that all of the alleles are in self._unmapped_alleles
        if not allele_set.issubset(self._unmapped_alleles):
            for a in allele_set:
                if not a in self._unmapped_alleles:
                    print(f"Could not find allele {a}")
            raise ValueError("[ERROR] We can only map alleles that were passed to the constructor - are you trying to map \"new\" alleles?")
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
            raise ValueError("[ERROR] We can only map alleles that were passed to the constructor - are you trying to map \"new\" alleles?")
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
            raise ValueError("[ERROR] We can only map alleles that were passed to the constructor - are you trying to map \"new\" alleles?")
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
        for allele in self._unmapped_alleles:
            if allele != allele.strip():
                unmapped_alleles = f"{unmapped_alleles}; warning \"{allele}\" has extra white space - check format"
        d = {"status": "unmapped", "count": n_unmapped, "alleles": unmapped_alleles}
        dlist.append(d)
        return pd.DataFrame(dlist)

    def has_unmapped_alleles(self):
        return len(self._unmapped_alleles) > 0

    def get_unmapped_alleles(self):
        return self._unmapped_alleles

    def get_mapped_allele_count(self):
        return len(self._var_d)


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
            if i._citation is not None:
                pmid = i.get_citation().pmid
                individual_id = self._format_pmid_id(identifier=i.id, pmid=pmid)
            else:
                individual_id = self._format_pmid_id(identifier=i.id, pmid=None)
            if individual_id not in self._individual_to_alleles_d:
                raise ValueError(f"Did not find {i.id} in our dictionary of individuals. Note that this function is intended to work with CaseTemplateEncoder")
            vlist = self._individual_to_alleles_d.get(individual_id)
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

    def get_var(self, v):
        """Get a Variant object that corresponds to v.

        :param v: an HGVS string or free-text representation of a chromosomal variant
        :type v: str
        :returns: corresponding Variant
        :rtype: Variant
        """
        return self._var_d.get(v)

    def get_variant_d(self):
        """
        :returns:dictionary with key: original string for allele, value: Variant object
        :rtype: Dict[str, Variant]
        """
        return self._var_d





