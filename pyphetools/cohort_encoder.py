import pandas as pd





class CohortEncoder:
    
    def __init__(self, df, id_to_primary_d, label_to_id_d):
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(id_to_primary_d, dict):
            raise ValueError(f"id_to_primary_d argument must be a dictionary but was {type(id_to_primary_d)}")
        if not isinstance(label_to_id_d, dict):
                raise ValueError(f"id_to_primary_d argument must be a dictionary but was {type(label_to_id_d)}")
        self._df = df
        self._id_to_primary_d = id_to_primary_d
        self._label_to_id_d = label_to_id_d