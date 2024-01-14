


class Citation:
    """encapsulate information about a citation that we add to the metadata for display

    :param pmid: PubMed identifier for the publication in which this individual was described (e.g. PMID:321..).
    :type pmid: str
    :param title: Title of the publication in which this individual was described.
    :type title: str
    """

    def __init__(self, pmid, title) -> None:
        self._pmid = pmid
        self._title = title


    @property
    def pmid(self):
        return self._pmid

    @property
    def title(self):
        return self._title