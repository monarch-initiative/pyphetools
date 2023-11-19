import unittest

import pytest

from src.pyphetools.creation import MetaData


class TestMetaData(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        hpo_version = "fake.version"
        pmid = "PMID:30945334"
        title = "Recurrent de novo MAPK8IP3 variants cause neurological phenotypes"
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199", pmid=pmid, pubmed_title=title)
        metadata.default_versions_with_hpo(version=hpo_version)
        cls._metadata = metadata.to_ga4gh()


    def test_created_by(self):
        expected_orcid = "ORCID:0000-0002-0736-9199"
        self.assertEqual(expected_orcid, self._metadata.created_by)

    def test_hpo_version(self):
        """We should retrieve Intellectual disability, mild (HP:0001256)"""
        mdata = self._metadata
        res = mdata.resources
        hpo_res = None
        for r in res:
            if r.id == "hp":
                hpo_res = r
        self.assertIsNotNone(hpo_res)
        self.assertEqual("fake.version", hpo_res.version)

    def test_has_five_resources(self):
        """
        the method default_versions_with_hpo adds a total of 5 ontologies to the MetaData
        """
        mdata = self._metadata
        self.assertEqual(5, len(mdata.resources))

    def test_external_reference(self):
        mdata = self._metadata
        self.assertEqual(1, len(mdata.external_references))
        eref = mdata.external_references[0]
        self.assertEqual("PMID:30945334", eref.id)
        self.assertEqual("https://pubmed.ncbi.nlm.nih.gov/30945334", eref.reference)
        self.assertEqual("Recurrent de novo MAPK8IP3 variants cause neurological phenotypes", eref.description)

    def test_pmid(self):
        # Test whether the pyphetools MetaData object returns the right PMID
        hpo_version = "fake.version"
        pmid = "PMID:30945334"
        title = "Recurrent de novo MAPK8IP3 variants cause neurological phenotypes"
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199", pmid=pmid, pubmed_title=title)
        self.assertEqual("PMID:30945334", metadata.get_pmid())


    def test_pmid_not_present(self):
        # Test whether the pyphetools MetaData object throws an error if we try to get a PMID that is not there
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199")
        with pytest.raises(ValueError) as v_e:
            pmid = metadata.get_pmid()

    def test_ga4gh_metadata_pmid(self):
        mdata = self._metadata
        self.assertEqual(1, len(mdata.external_references))
        eref = mdata.external_references[0]
        self.assertEqual("PMID:30945334", eref.id)


