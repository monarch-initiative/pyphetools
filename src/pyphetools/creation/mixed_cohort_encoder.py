from math import isnan
from typing import List, Dict

import pandas as pd

from . import Individual
from .abstract_encoder import AbstractEncoder
from .age_column_mapper import AgeColumnMapper
from .constants import Constants
from .hpo_cr import HpoConceptRecognizer
from .sex_column_mapper import SexColumnMapper


class MixedCohortEncoder(AbstractEncoder):
    """Map a table of data to Individual/GA4GH Phenopacket Schema objects. This class should be used instead of CohortMapper
       if the table has different diseases or different pubmed references for each row.

        Encode a cohort of individuals with clinical data in a table as a collection of GA4GH Phenopackets
        This classes uses a collection of ColumnMapper objects to map a table using the
        get_individuals or output_phenopackets methods.

        The column_mapper_d is a dictionary with key=column names, and value=Mapper objects. These mappers are responsible
        for mapping HPO terms. The agemapper and the sexmapper are specialized for the respective columns. The
        variant mapper is useful if there is a single variant column that is all HGVS or structural variants. In some
        cases, it is preferable to use the variant_dictionary, which has key=string (cell contents) and value=Hgvs or
        StructuralVariant object.

        :param df: tabular data abotu a cohort
        :type df: pd.DataFrame
        :param hpo_cr: HpoConceptRecognizer for text mining
        :type hpo_cr: pyphetools.creation.HpoConceptRecognizer
        :param column_mapper_d: Dictionary with key: Column name, value: ColumnMapper object
        :type column_mapper_d: Dict[pyphetools.creation.ColumnMapper]
        :param individual_column_name: label of column with individual/proband/patient identifier
        :type individual_column_name: str
        :param disease_id_mapper: label of column with disease id
        :type disease_id_mapper: str
        :param metadata: GA4GH MetaData object
        :type metadata: PPkt.MetaData
        :param variant_mapper: column mapper for HGVS-encoded variant column. Defaults to None.
        :type variant_mapper: pyphetools.creation.VariantColumnMapper
        :param agemapper:Mapper for the Age column. Defaults to AgeColumnMapper.not_provided()
        :type agemapper: pyphetools.creation.AgeColumnMapper
        :param sexmapper: Mapper for the Sex column. Defaults to SexColumnMapper.not_provided().
        :type sexmapper: pyphetools.creation.SexColumnMapper
        :param pmid_column: name of column with PubMed identifier for the row
        :type pmid_column: str
        :raises: ValueError - several of the input arguments are checked.
        """
    def __init__(self,
                 df,
                 hpo_cr,
                 column_mapper_d,
                 individual_column_name,
                 disease_id_mapper,
                 metadata,
                 pmid_column,
                 title_column=None,
                 variant_mapper=None,
                 agemapper=AgeColumnMapper.not_provided(),
                 sexmapper=SexColumnMapper.not_provided(),
                 delimiter=None):
        """Constructor
        """
        super().__init__(metadata=metadata)
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
        self._df = df.astype(str)
        self._column_mapper_d = column_mapper_d
        self._id_column_name = individual_column_name
        self._age_mapper = agemapper
        self._sex_mapper = sexmapper
        self._disease_id_mapper = disease_id_mapper
        self._pmid_column = pmid_column
        self._title_column = title_column
        self._variant_mapper = variant_mapper
        self._delimiter = delimiter
        ontology = hpo_cr.get_hpo_ontology()
        if ontology is None:
            raise ValueError("ontology cannot be None")


    def get_individuals(self) -> List[Individual]:
        """Get a list of all Individual objects in the cohort

        :returns: a list of all Individual objects in the cohort
        :rtype: List[Individual]
        """
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        age_column_name = self._age_mapper.get_column_name()
        sex_column_name = self._sex_mapper.get_column_name()
        disease_column_name = self._disease_id_mapper.get_column_name()
        if self._variant_mapper is None:
            variant_colname = None
            genotype_colname = None
        else:
            variant_colname = self._variant_mapper.get_variant_column_name()
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
                    print(f"Warning: Could not parse age {ee}. Setting age to \"not provided\"")
                    age = Constants.NOT_PROVIDED
            if sex_column_name == Constants.NOT_PROVIDED:
                sex = self._sex_mapper.map_cell(Constants.NOT_PROVIDED)
            else:
                sex_cell_contents = row[sex_column_name]
                sex = self._sex_mapper.map_cell(sex_cell_contents)
            pmid = row[self._pmid_column]
            if self._title_column is not None:
                title = row[self._title_column]
            else:
                title = None
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
                if genotype_colname is not None:
                    genotype_cell_contents = row[genotype_colname]
                else:
                    genotype_cell_contents = None
                if self._variant_mapper is not None:
                    interpretation_list = self._variant_mapper.map_cell(variant_cell_contents, genotype_cell_contents)
                else:
                    interpretation_list = []
            else:
                interpretation_list = []
            disease_cell_contents = row[disease_column_name]
            if disease_cell_contents is None:
                raise ValueError(f"Could not extract disease identifier for row {row}")
            disease = self._disease_id_mapper.map_cell(disease_cell_contents)
            indi = Individual(individual_id=individual_id,
                                  sex=sex,
                                  age=age,
                                  hpo_terms=hpo_terms,
                                  pmid=pmid,
                                  title=title,
                                  interpretation_list=interpretation_list,
                                  disease=disease)
            individuals.append(indi)
        return individuals
