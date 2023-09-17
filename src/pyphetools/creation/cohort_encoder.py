import pandas as pd
from math import isnan
from typing import List
from collections import defaultdict
import os

from .age_column_mapper import AgeColumnMapper
from .constants import Constants
from .hpo_cr import HpoConceptRecognizer
from .individual import Individual
from .sex_column_mapper import SexColumnMapper
from .variant_column_mapper import VariantColumnMapper


class CohortEncoder:
    """Encode a cohort of individuals with clinical data in a table as a collection of GA4GH Phenopackets
    This classes uses a collection of ColumnMapper objects to map a table using the
    get_individuals or output_phenopackets methods.
    """

    def __init__(self, 
                 df, 
                 hpo_cr, 
                 column_mapper_d, 
                 individual_column_name, 
                 metadata,
                 agemapper=AgeColumnMapper.not_provided(), 
                 sexmapper=SexColumnMapper.not_provided(), 
                 variant_mapper=None, 
                 pmid=None):
        """_summary_

        Args:
            df (pd.DataFrame): tabular data abotu a cohort
            hpo_cr (HpoConceptRecognizer): HPO concept recognizer
            column_mapper_d (dict): Dictionary with key: Column name, value: ColumnMapper object
            individual_column_name (str): label of column with individual/proband/patient identifier
            metadata (Object): GA4GH MetaData object
            agemapper (AgeColumnMapper, optional): Mapper for the Age column. Defaults to AgeColumnMapper.not_provided().
            sexmapper (SexColumnMapper, optional): Mapper for the Sex column. Defaults to SexColumnMapper.not_provided().
            variant_mapper (VariantColumnMapper, optional): mapper for HGVS-encoded variant column. Defaults to None.
            non_hgvs_variant_map (dict, optional): key: string in the variant column value: VarMapper for converting the string to GA4GH VariationDescriptor . Defaults to empty defaultdict().
            pmid (str, optional): PubMed identifier for the cohort. Defaults to None.

        Raises:
            ValueError: several of the input arguments are checked.
        """
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(
                "concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._hpo_concept_recognizer = hpo_cr
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(column_mapper_d, dict):
            raise ValueError(f"column_mapper_d argument must be a dictionary but was {type(column_mapper_d)}")
        if not isinstance(individual_column_name, str):
            raise ValueError(f"individual_column_name argument must be a string but was {type(individual_column_name)}")
        if variant_mapper is not None and not isinstance(variant_mapper, VariantColumnMapper):
            raise ValueError(f"variant_mapper argument must be VariantColumnMapper but was {type(variant_mapper)}")
        if metadata is None:
            raise ValueError("Must pass a metadata object to constructor")
        # the following workaround is needed because isinstance gets confused about the two following classes
        elif str(type(metadata)) == "<class 'phenopackets.schema.v2.core.meta_data_pb2.MetaData'>":
            self._metadata = metadata
        elif str(type(metadata)) == "<class 'pyphetools.creation.metadata.MetaData'>":
            self._metadata = metadata.to_ga4gh()
        else:
            raise ValueError(F"Malformed metadata argument of type {type(metadata)}")
        self._df = df.astype(str)
        self._column_mapper_d = column_mapper_d
        self._id_column_name = individual_column_name
        self._age_mapper = agemapper
        self._sex_mapper = sexmapper
        self._disease_id = None
        self._disease_label = None
        self._variant_mapper = variant_mapper
        self._pmid = pmid
        self._disease_dictionary = None

    def preview_dataframe(self):
        """
        Generate a dataframe with a preview of the parsed contents
        """
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        age_column_name = self._age_mapper.get_column_name()
        sex_column_name = self._sex_mapper.get_column_name()
        for index, row in df.iterrows():
            individual_id = row[self._id_column_name]
            if age_column_name == Constants.NOT_PROVIDED:
                age = Constants.NOT_PROVIDED
            else:
                age_cell_contents = row[age_column_name]
                age = self._age_mapper.map_cell(age_cell_contents)
            sex_cell_contents = row[sex_column_name]
            sex = self._sex_mapper.map_cell(sex_cell_contents)
            hpo_terms = []
            for column_name, column_mapper in self._column_mapper_d.items():
                cell_contents = row[column_name]
                # Empty cells are often represented as float non-a-number by Pandas
                if isinstance(cell_contents, float) and isnan(cell_contents):
                    continue
                terms = column_mapper.map_cell(row[column_name])
                hpo_terms.extend(terms)
            hpo_string = "\n".join([h.to_string() for h in hpo_terms])
            d = {'id': individual_id,
                 'sex': sex,
                 'age': age,
                 'phenotypic features': hpo_string}
            individuals.append(d)
        df = pd.DataFrame(individuals)
        return df.set_index('id')

    def set_disease(self, disease_id, label):
        """_summary_
        If all patients in the cohort have the same disease we can set it with this method
        Args:
            disease_id (str): disease identifier, e.g., OMIM:600123
            label (str): disease name
        """
        self._disease_id = disease_id
        self._disease_label = label
        self._disease_dictionary = None

    def set_disease_dictionary(self, disease_d):
        self._disease_dictionary = disease_d
        self._disease_id = None
        self._disease_label = None

    def get_individuals(self) -> List[Individual]:
        """Get a list of all Individual objects in the cohort
        """
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        age_column_name = self._age_mapper.get_column_name()
        sex_column_name = self._sex_mapper.get_column_name()
        if self._variant_mapper is None:
            variant_colname = None
            genotype_colname = None
        else:
            variant_colname = self._variant_mapper.get_column_name()
            genotype_colname = self._variant_mapper.get_genotype_colname()
        for index, row in df.iterrows():
            individual_id = row[self._id_column_name]
            if age_column_name == Constants.NOT_PROVIDED:
                age = Constants.NOT_PROVIDED
            else:
                age_cell_contents = row[age_column_name]
                try:
                    age = self._age_mapper.map_cell(age_cell_contents)
                except Exception as ee:
                    print(f"Error: Could not parse age {ee}")
                    age = Constants.NOT_PROVIDED
            if sex_column_name == Constants.NOT_PROVIDED:
                sex = self._sex_mapper.map_cell(Constants.NOT_PROVIDED)
            else:
                sex_cell_contents = row[sex_column_name]
                sex = self._sex_mapper.map_cell(sex_cell_contents)
            hpo_terms = []
            for column_name, column_mapper in self._column_mapper_d.items():
                if column_name not in df.columns:
                    raise ValueError(f"Did not find column name '{column_name}' in dataframe -- check spelling!")
                cell_contents = row[column_name]
                # Empty cells are often represented as float non-a-number by Pandas
                if isinstance(cell_contents, float) and isnan(cell_contents):
                    continue
                terms = column_mapper.map_cell(cell_contents)
                hpo_terms.extend(terms)
            if variant_colname is not None:
                variant_cell_contents = row[variant_colname]
                interpretation_list = []
                if genotype_colname is not None:
                    genotype_cell_contents = row[genotype_colname]
                else:
                    genotype_cell_contents = None
                interpretation_list = self._variant_mapper.map_cell(variant_cell_contents, genotype_cell_contents)
            else:
                interpretation_list = []
            if self._disease_dictionary is not None and self._disease_id is None and self._disease_label is None:
                if individual_id not in self._disease_dictionary:
                    raise ValueError(f"Could not find disease link for {individual_id}")
                disease = self._disease_dictionary.get(individual_id)
                disease_id = disease.get('id')
                disease_label = disease.get('label')
                indi = Individual(individual_id=individual_id, 
                                  sex=sex, 
                                  age=age, 
                                  hpo_terms=hpo_terms,
                                  pmid=self._pmid,
                                  interpretation_list=interpretation_list,
                                  disease_id=disease_id, 
                                  disease_label=disease_label)
                individuals.append(indi)
            elif self._disease_dictionary is None and self._disease_id is not None and self._disease_label is not None:
                indi = Individual(individual_id=individual_id, 
                                  sex=sex, 
                                  age=age, 
                                  hpo_terms=hpo_terms,
                                  pmid=self._pmid,
                                  interpretation_list=interpretation_list, disease_id=self._disease_id,
                                  disease_label=self._disease_label)
                individuals.append(indi)
            else:
                raise ValueError(f"Could not find disease data for '{individual_id}'")
        return individuals

    def output_phenopackets(self, outdir="phenopackets"):
        """Output data about all individuals as GA4GH phenopackets

        Args:
            outdir (str): name of directory to write phenopackets (default: 'phenopackets')
        """
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        individual_list = self.get_individuals()
        written = Individual.output_individuals_as_phenopackets(individual_list=individual_list,
                                                                metadata=self._metadata,
                                                                pmid=self._pmid,
                                                                outdir=outdir)
        print(f"Wrote {written} phenopackets to {outdir}")
