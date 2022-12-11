import pandas as pd

from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer





class CohortEncoder:
    
    def __init__(self, df, hpo_cr, column_mapper_d,  metadata):
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(f"hpo_cr argument must be a HpoConceptRecognizer but was {type(hpo_cr)}")
        if not isinstance(column_mapper_d, dict):
            raise ValueError(f"column_mapper_d argument must be a diction but was {type(column_mapper_d)}")
        if not isinstance(metadata, dict):
            raise ValueError(f"metadata argument must be a diction but was {type(metadata)}")
        self._df = df
        self._hpo_concept_recognizer = hpo_cr
        self._column_mapper_d = column_mapper_d
        self._id_column = metadata.get('id')
        self._sex_column = metadata.get('sex')
        self._age_column = metadata.get('age')
        
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
                terms = column_mapper.map_cell(row[column_name])
                hpo_terms.extend(terms)
            hpo_string = "\n".join([h.to_string() for h in hpo_terms])
            d = {'id': individual_id,
                 'sex': sex,
                 'age': age,
                 'phenotypic features': hpo_string}
            individuals.append(d)
        return pd.DataFrame(individuals)
            


   