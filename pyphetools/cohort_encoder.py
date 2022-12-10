import pandas as pd

from .column_mapper import ColumnMapper
from .hpo_cr import HpoConceptRecognizer





class CohortEncoder:
    
    def __init__(self, df, hpo_cr):
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(f"hpo_cr argument must be a HpoConceptRecognizer but was {type(hpo_cr)}")
        self._df = df
        self._hpo_concept_recognizer = hpo_cr


   