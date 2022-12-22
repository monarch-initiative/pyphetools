


class HpTerm:
    def __init__(self, id, label, observed=True, measured=True):
        if id is None or len(id) == 0 or not id.startswith("HP"):
            raise ValueError(f"invalid id argument: '{id}'")
        if label is None or len(label) == 0:
            raise ValueError(f"invalid label argument: '{label}'")
        self._id = id
        self._label = label
        self._observed = observed
        self._measured = measured
        
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