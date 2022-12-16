import pandas as pd
from math import isnan
from typing import List

from .column_mapper import ColumnMapper
from .variant_column_mapper import VariantColumnMapper
from .hpo_cr import HpoConceptRecognizer
from .individual import Individual




class CohortEncoder:
    
    def __init__(self, df, hpo_cr, column_mapper_d,  individual_d, variant_mapper=None):
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(f"hpo_cr argument must be a HpoConceptRecognizer but was {type(hpo_cr)}")
        if not isinstance(column_mapper_d, dict):
            raise ValueError(f"column_mapper_d argument must be a diction but was {type(column_mapper_d)}")
        if not isinstance(individual_d, dict):
            raise ValueError(f"metadata argument must be a diction but was {type(individual_d)}")
        if variant_mapper is not None and not isinstance(variant_mapper, VariantColumnMapper):
            raise ValueError(f"variant_mapper argument must be VariantColumnMapper but was {type(variant_mapper)}")
        self._df = df
        self._hpo_concept_recognizer = hpo_cr
        self._column_mapper_d = column_mapper_d
        self._id_column = individual_d.get('id')
        self._sex_column = individual_d.get('sex')
        self._age_column = individual_d.get('age')
        self._disease_id = None
        self._disease_label = None
        self._variant_mapper = variant_mapper
        
    def preview_dataframe(self):
        """
        Generate a dataframe with a preview of the parsed contents
        """
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        for index, row in df.iterrows():
            individual_id = row[self._id_column]
            sex = row[self._sex_column]
            age = row[self._age_column]
            hpo_terms = []
            for column_name, column_mapper in self._column_mapper_d.items():
                cell_contents = row[column_name]
                ## Empty cells are often represented as float non-a-number by Pandas
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
            id (str): disease identifier, e.g., OMIM:600123
            label (str): disease name
        """
        self._disease_id = disease_id
        self._disease_label = label
    
    
    def get_individuals(self) -> List[Individual]:
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        if self._variant_mapper is None:
            variant_colname = None
        else:
            variant_colname = self._variant_mapper.get_column_name()
        for index, row in df.iterrows():
            individual_id = row[self._id_column]
            sex = row[self._sex_column]
            age = row[self._age_column]
            hpo_terms = []
            for column_name, column_mapper in self._column_mapper_d.items():
                cell_contents = row[column_name]
                ## Empty cells are often represented as float non-a-number by Pandas
                if isinstance(cell_contents, float) and isnan(cell_contents):
                    continue
                terms = column_mapper.map_cell(cell_contents)
                hpo_terms.extend(terms)
            if variant_colname is not None:
                variant_col = row[variant_colname]
                variant_list = self._variant_mapper.map_cell(variant_col)
            else:
                variant_list = []
            print("size of variant_list is {len(variant_list)}")
            indi = Individual(individual_id=individual_id, sex=sex, age=age, hpo_terms=hpo_terms, variant_list=variant_list,
                              disease_id=self._disease_id, disease_label=self._disease_label)
            individuals.append(indi)
        return individuals
        
    
            


   