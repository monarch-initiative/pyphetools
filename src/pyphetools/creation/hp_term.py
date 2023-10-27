import pandas as pd
import phenopackets 
from .constants import Constants

class HpTerm:
    """
    Class to represent a phenotypic observation as an HPO term with optional modifiers

    :param hpo_id: a Human Phenotype Ontology (HPO) identifier such as HP:0001166
    :type hpo_id: str
    :param label: The HPO label that corresponds to the id (note: This class does not check for correct match)
    :type label: str
    :param observed: a boolean that indicates whether the HPO term was observed (True) or excluded (False)
    :type observed: bool
    :param measured: a boolean that indicates whether the HPO was measured (True) or not explicitly measured (False)
    :type measured: bool
    :param onset: an ISO8601 string representing the age of onset, optional
    :type onset: str
    :param resolution: an ISO8601 string representing the age of resolution, optional
    :type resolution: str
    """
    def __init__(self, hpo_id, label, observed=True, measured=True, onset=Constants.NOT_PROVIDED, resolution=None):
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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other._id and self._label == other._label and self._measured == other._measured and self._onset == other._onset and self._resolution == other._resolution
        else:
            return NotImplemented
        
    def __hash__(self):
        return hash((self._id, self._label, self._observed, self._measured, self._onset, self._resolution))
        
    @property
    def id(self):
        """
        :returns: The HPO identifier, e.g., HP:0001166
        :rtype: str
        """
        return self._id
    
    @property
    def label(self):
        """
        :returns: The HPO label, e.g., Arachnodactyly
        :rtype: str
        """
        return self._label
    
    @property
    def observed(self):
        return self._observed
    
    @property
    def measured(self):
        """
        :returns: True iff a measurement to assess this abnormality (HpTerm) was performed
        :rtype: bool
        """
        return self._measured
    
    @property
    def onset(self):
        """
        :returns: iso8601 string representing the age this abnormality first was observed
        :rtype: str, optional
        """
        return self._onset

    def set_onset(self, onset):
        self._onset = onset
    
    @property
    def resolution(self):
        """
        :returns: iso8601 string representing the age this abnormality resolved
        :rtype: str, optional
        """
        return self._resolution
    
    @property
    def display_value(self):
        """
        :returns: One of three strings describing the status of the term: "not measured", "excluded", or "observed"
        :rtype: str
        """
        if not self._measured:
            return "not measured"
        if not self._observed:
            return "excluded"
        else:
            return "observed"
    
    @property
    def hpo_term_and_id(self):
        """
        :returns: A string such as Arachnodactyly (HP:0001166) for display
        :rtype: str
        """
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
        """
        Sets the current term to excluded (i.e., the abnormality was sought but explicitly ruled out clinically)
        """
        self._observed = False
        
    def to_phenotypic_feature(self):
        """
        :returns: A GA4GH PhenotypcFeature corresponding to this HpTerm
        :rtype: phenopackets.PhenotypicFeature
        """
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
