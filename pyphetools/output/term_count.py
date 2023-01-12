from hpotk.model import TermId


class TermCount:

    def __init__(self, id) -> None:
        if not isinstance(id, TermId):
            raise ValueError(f"id argument must be TermId but was {type(id)}")
        self._hpo_id = id
        self._count = 0

    def increment(self):
        self._count += 1

    @property
    def hpo_id(self):
        return self._hpo_id

    @property
    def count(self):
        return self._count