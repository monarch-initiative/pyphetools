


class Citation:
    """encapsulate information about a citation that we add to the metadata for display

    :param pmid: PubMed identifier for the publication in which this individual was described (e.g. PMID:321..).
    :type pmid: str
    :param title: Title of the publication in which this individual was described.
    :type title: str
    """

    def __init__(self, pmid:str, title:str) -> None:
        if pmid is None or isinstance(pmid, float) or not pmid.startswith("PMID"):
            raise ValueError(f"Could not find PubMed identifier")
        if title is None or isinstance(title, float) or len(title) < 5:
            raise ValueError(f"Could not find valid title")
        self._pmid = pmid
        self._title = title


    @property
    def pmid(self):
        return self._pmid

    @property
    def title(self):
        return self._title