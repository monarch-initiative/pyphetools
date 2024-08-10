import pandas as pd
from math import isnan
import typing

from .abstract_encoder import AbstractEncoder
from .age_column_mapper import AgeColumnMapper
from .column_mapper import ColumnMapper
from .constants import Constants
from .disease import Disease
from .hpo_cr import HpoConceptRecognizer
from .individual import Individual
from .sex_column_mapper import SexColumnMapper
from .variant_column_mapper import VariantColumnMapper


class CohortEncoder(AbstractEncoder):
    """Map a table of data to Individual/GA4GH Phenopacket Schema objects

    Encode a cohort of individuals with clinical data in a table as a collection of GA4GH Phenopackets
    This classes uses a collection of ColumnMapper objects to map a table using the
    get_individuals or output_phenopackets methods.

    The column_mapper_d is a dictionary with key=column names, and value=Mapper objects. These mappers are responsible
    for mapping HPO terms. The agemapper and the sexmapper are specialized for the respective columns. The
    variant mapper is useful if there is a single variant column that is all HGVS or structural variants. In some
    cases, it is preferable to use the variant_dictionary, which has key=string (cell contents) and value=Hgvs or
    StructuralVariant object.

    :param df: tabular data about a cohort
    :type df: pd.DataFrame
    :param hpo_cr: HpoConceptRecognizer for text mining
    :type hpo_cr: pyphetools.creation.HpoConceptRecognizer
    :param column_mapper_list: list of ColumnMapper objects
    :type column_mapper_list: List[pyphetools.creation.ColumnMapper]
    :param individual_column_name: label of column with individual/proband/patient identifier
    :type individual_column_name: str
    :param metadata: GA4GH MetaData object
    :type metadata: PPkt.MetaData
    :param age_of_onset_mapper:Mapper for the Age of onset column. Defaults to AgeColumnMapper.not_provided()
    :type age_of_onset_mapper: pyphetools.creation.AgeColumnMapper
    :param age_at_last_encounter_mapper:Mapper for the Age at last clinical encounter column. Defaults to AgeColumnMapper.not_provided()
    :type age_at_last_encounter_mapper: pyphetools.creation.AgeColumnMapper
    :param sexmapper: Mapper for the Sex column. Defaults to SexColumnMapper.not_provided().
    :type sexmapper: pyphetools.creation.SexColumnMapper
    :param variant_mapper: column mapper for HGVS-encoded variant column.
    :type variant_mapper: pyphetools.creation.VariantColumnMapper
    :raises: ValueError - several of the input arguments are checked.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 hpo_cr: HpoConceptRecognizer,
                 column_mapper_list: typing.List[ColumnMapper],
                 individual_column_name: str,
                 metadata,
                 age_of_onset_mapper: AgeColumnMapper = AgeColumnMapper.not_provided(),
                 age_at_last_encounter_mapper: AgeColumnMapper = AgeColumnMapper.not_provided(),
                 sexmapper: SexColumnMapper = SexColumnMapper.not_provided(),
                 variant_mapper: VariantColumnMapper = None,
                 delimiter: str = None):
        """Constructor
        """
        super().__init__(metadata=metadata)
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(
                "concept_recognizer argument must be HpoConceptRecognizer but was {type(concept_recognizer)}")
        self._hpo_concept_recognizer = hpo_cr
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(column_mapper_list, list):
            raise ValueError(f"column_mapper_list argument must be a list but was {type(column_mapper_list)}")
        if not isinstance(individual_column_name, str):
            raise ValueError(f"individual_column_name argument must be a string but was {type(individual_column_name)}")
        if variant_mapper is not None and not isinstance(variant_mapper, VariantColumnMapper):
            raise ValueError(f"variant_mapper argument must be VariantColumnMapper but was {type(variant_mapper)}")
        self._df = df.astype(str)
        self._column_mapper_list = column_mapper_list
        self._id_column_name = individual_column_name
        self._age_of_onset_mapper = age_of_onset_mapper
        self._age_at_last_encounter_mapper = age_at_last_encounter_mapper
        self._sex_mapper = sexmapper
        self._disease = None
        self._variant_mapper = variant_mapper
        self._disease_dictionary = None
        self._delimiter = delimiter

    def preview_dataframe(self):
        """
        Generate a dataframe with a preview of the parsed contents

        :returns: a DataFrame representing the cohort to check results
        :rtype: pd.DataFrame
        """
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        age_column_name = self._age_of_onset_mapper.get_column_name()
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
            for column_mapper in self.__column_mapper_list:
                column_name = column_mapper.get_column_name()
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

    def set_disease(self, disease: Disease):
        """Set the disease diagnosis for all patients in the cohort

        If all patients in the cohort have the same disease we can set it with this method
        :param disease: Disease diagnosis for the individuals in this cohort
        :type disease: Disease
        """
        self._disease = disease
        self._disease_dictionary = None

    def set_disease_dictionary(self,
                               disease_d: typing.Dict[str, Disease]):
        """Set the dictionary of disease ontology terms

        For tables with multiple different diseases, we provide a dictionary that has as key
        the string used in the original table and as value
        """
        self._disease_dictionary = disease_d
        self._disease = None

    def _get_age(row: pd.Series, mapper: AgeColumnMapper):
        import math
        column_name = mapper.get_column_name()
        if column_name == Constants.NOT_PROVIDED:
            return None
        age_cell_contents = row[column_name]
        if isinstance(age_cell_contents, float) and math.isnan(age_cell_contents):
            return None
        try:
            age = mapper.map_cell(age_cell_contents)
        except Exception as ee:
            print(f"Warning: Could not parse age {ee}. Setting age to \"not provided\"")
            age = None
        return age

    def get_individuals(self) -> typing.List[Individual]:
        """Get a list of all Individual objects in the cohort

        :returns: a list of all Individual objects in the cohort
        :rtype: List[Individual]
        """
        # make sure indexes pair with number of rows, if needed
        if not self._df.index.name in self._df.columns:
            df = self._df.reset_index()
        individuals = []
        sex_column_name = self._sex_mapper.get_column_name()
        if self._variant_mapper is None:
            variant_colname = None
            genotype_colname = None
        else:
            variant_colname = self._variant_mapper.get_variant_column_name()
            genotype_colname = self._variant_mapper.get_genotype_colname()
        for index, row in df.iterrows():
            individual_id = row[self._id_column_name]
            age_of_onset = CohortEncoder._get_age(row, self._age_of_onset_mapper)
            age_last_encounter = CohortEncoder._get_age(row, self._age_at_last_encounter_mapper)
            if sex_column_name == Constants.NOT_PROVIDED:
                sex = self._sex_mapper.map_cell(Constants.NOT_PROVIDED)
            else:
                sex_cell_contents = row[sex_column_name]
                sex = self._sex_mapper.map_cell(sex_cell_contents)
            hpo_terms = []
            for column_mapper in self._column_mapper_list:
                column_name = column_mapper.get_column_name()
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
            if self._disease_dictionary is not None and self._disease is None:
                if individual_id not in self._disease_dictionary:
                    raise ValueError(f"Could not find disease link for {individual_id}")
                disease = self._disease_dictionary.get(individual_id)
                indi = Individual(individual_id=individual_id,
                                  sex=sex,
                                  age_of_onset=age_of_onset,
                                  age_at_last_encounter=age_last_encounter,
                                  hpo_terms=hpo_terms,
                                  citation=self._metadata.get_citation(),
                                  interpretation_list=interpretation_list,
                                  disease=disease)
            elif self._disease_dictionary is None and self._disease is not None:
                indi = Individual(individual_id=individual_id,
                                  sex=sex,
                                  age_of_onset=age_of_onset,
                                  age_at_last_encounter=age_last_encounter,
                                  hpo_terms=hpo_terms,
                                  citation=self._metadata.get_citation(),
                                  interpretation_list=interpretation_list,
                                  disease=self._disease)
            else:
                raise ValueError(f"Could not find disease data for '{individual_id}'")
            individuals.append(indi)
        if self._age_of_onset_mapper.has_error():
            print(self._age_of_onset_mapper.error_summary())
        if self._age_at_last_encounter_mapper.has_error():
            print(self._age_at_last_encounter_mapper.error_summary())
        if self._sex_mapper.has_error():
            print(self._sex_mapper.error_summary())
        return individuals
