import pandas as pd
import phenopackets 
from .constants import Constants

class HpTerm:
    def __init__(self, hpo_id, label, observed=True, measured=True, onset=None, resolution=None):
        if hpo_id is None or len(hpo_id) == 0 or not hpo_id.startswith("HP"):
            raise ValueError(f"invalid id argument: '{hpo_id}'")
        if label is None or len(label) == 0:
            raise ValueError(f"invalid label argument: '{label}'")
        self._id = hpo_id
        self._label = label
        self._observed = observed
        self._measured = measured
        if onset is None:
            self._onset = Constants.NOT_PROVIDED
        else:
            self._onset = onset
        if resolution is None:
            self._resolution = Constants.NOT_PROVIDED
        else:
            self._resolution = resolution
        
    def __hash__(self):
        return hash((self._id, self._label, self._observed, self._measured))
        
    @property
    def id(self):
        return self._id
    
    @property
    def label(self):
        return self._label
    
    @property
    def observed(self):
        return self._observed
    
    @property
    def measured(self):
        return self._measured
    
    @property
    def onset(self):
        return self._onset
    
    @property
    def resolution(self):
        return self._resolution
    
    @property
    def display_value(self):
        if not self._measured:
            return "not measured"
        if not self._observed:
            return "excluded"
        else:
            return "observed"
    
    @property
    def hpo_term_and_id(self):
        return f"{self._label} ({self._id})"
    
    def __str__(self) -> str:
        if not self._measured:
            return f"not measured: {self._label} ({self._id})"
        elif not self._observed:
            return f"excluded: {self._label} ({self._id})"
        else:
            return f"{self._label} ({self._id})"
    
    def to_string(self):
        return self.__str__()

    def excluded(self):
        self._observed = False
        
    def to_phenotypic_feature(self):
        pf = phenopackets.PhenotypicFeature()
        pf.type.id = self._id
        pf.type.label = self._label
        if not self._observed:
            pf.excluded = True
        if self._onset != Constants.NOT_PROVIDED:
            pf.onset.age.iso8601duration = self._onset
        if self._resolution != Constants.NOT_PROVIDED:
            pf.resolution.age.iso8601duration = self._resolution
        return pf


    @staticmethod
    def term_list_to_dataframe(hpo_list):
        if not isinstance(hpo_list, list):
            raise ValueError(f"hpo_list argument must be a list but was {type(hpo_list)}")
        if len(hpo_list) > 0:
            hpo1 = hpo_list[0]
            if not isinstance(hpo1, HpTerm):
                raise ValueError(f"hpo_list argument must consist of HpTerm objects but had {type(hpo1)}")
        if len(hpo_list) == 0:
            return pd.DataFrame(columns=['Col1', 'Col2', 'Col3'])
        items = []
        for hp in hpo_list:
            d = { "id": hp.id, "label": hp.label, "observed":hp.observed, "measured": hp.measured }
            items.append(d)
        return pd.DataFrame(items)
