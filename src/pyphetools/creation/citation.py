from ..pp.v202 import ExternalReference as ExternalReference202

class Citation:
    """encapsulate information about a citation that we add to the metadata for display
    """

    def __init__(self, pmid:str, title:str) -> None:
        """
        :param pmid: PubMed identifier for the publication in which this individual was described (e.g. PMID:321..).
        :type pmid: str
        :param title: Title of the publication in which this individual was described.
        :type title: str
        """
        if pmid is None or isinstance(pmid, float) or not pmid.startswith("PMID"):
            raise ValueError(f"Could not find PubMed identifier")
        if title is None or isinstance(title, float) or len(title) < 5:
            raise ValueError(f"Could not find valid title")
        self._pmid = pmid
        self._title = title

    @property
    def pmid(self) -> str:
        return self._pmid

    @property
    def title(self) -> str:
        return self._title
    
    def to_external_reference(self) -> ExternalReference202:
        """
        :returns: an ExternalReference object representing this PubMed citation
        :rtype: ExternalReference202
        """
        pm_number = self._pmid.replace("PMID:", "")
        pm_url = f"https://pubmed.ncbi.nlm.nih.gov/{pm_number}" 
        return ExternalReference202(id=self._pmid,
                                    reference=pm_url,
                                    description=self._title)
    