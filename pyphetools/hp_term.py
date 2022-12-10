


class HpTerm:
    def __init__(self, id, label):
        if id is None or len(id) == 0 or not id.startswith("HP"):
            raise ValueError(f"invalid id argument: '{id}'")
        if label is None or len(label) == 0:
            raise ValueError(f"invalid label argument: '{label}'")
        self._id = id
        self._label = label
        
    @property
    def id(self):
        return self._id
    
    @property
    def label(self):
        return self._label
    
    def __str__(self) -> str:
        return f"{self._label} ({self._id})"
    
    def to_string(self):
        return self.__str__()