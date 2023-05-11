from hpotk.model import TermId


class TermCount:

    def __init__(self, tid) -> None:
        """Counts the number of usages of an ontology term

        Args:
            tid: An ontology term identifier
        """
        if not isinstance(tid, TermId):
            raise ValueError(f"id argument must be TermId but was {type(tid)}")
        self._hpo_id = tid
        self._count = 0

    def increment(self):
        self._count += 1

    @property
    def hpo_id(self):
        return self._hpo_id

    @property
    def count(self):
        return self._count
