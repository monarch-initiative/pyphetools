import pytest

from pyphetools.creation import Citation
from pyphetools.pp.v202 import ExternalReference as ExternalReference202

class TestCitation:


    def test_create_citation(self):
        PMID = "PMID:25293717"
        title = "Somatic neurofibromatosis type 1 (NF1) inactivation events in cutaneous neurofibromas of a single NF1 patient"
        citation = Citation(pmid=PMID, title=title)
        ext_ref = citation.to_external_reference()
        assert isinstance(ext_ref, ExternalReference202)
        assert ext_ref.id == PMID
        assert ext_ref.description == title
        expected_url = "https://pubmed.ncbi.nlm.nih.gov/25293717"
        assert ext_ref.reference == expected_url
       