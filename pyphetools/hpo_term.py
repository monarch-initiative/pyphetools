



class HpoTerm:
    def __init__(self, id, label) -> None:
        self._id = id
        self._label = label
    
    @property
    def id(self):
        return self._id
    
    @property
    def label(self):
        return self._label