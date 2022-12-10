


class HpTerm:
    def __init__(self, id, label):
        if id is None or len(id) == 0 or not id.startswith("HP"):
            raise ValueError("invalid id argument: '{id}'")
        if label is None or len(label) == 0:
            raise ValueError("invalid label argument: '{label}'")
        self._id = id
        self._label = label
        
    @property
    def id(self):
        return self._id
    
    @property
    def label(self):
        return self._label