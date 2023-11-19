import time
from collections import defaultdict

import phenopackets as PPKt
from google import protobuf


class Resource:
    def __init__(self, resource_id, name, namespace_prefix, iriprefix, url, version) -> None:
        self._id = resource_id
        self._name = name
        self._namespace_prefix = namespace_prefix
        self._iri_prefix = iriprefix
        self._url = url
        self._version = version

    def to_ga4gh(self):
        pass

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def namespace_prefix(self):
        return self._namespace_prefix

    @property
    def iri_prefix(self):
        return self._iri_prefix

    @property
    def url(self):
        return self._url

    @property
    def version(self):
        return self._version


# current versions of ontologies used for these phenopackets
# if the user does not specify versions, these versions will be
# used.
# for our purposes, the one version that will change a lot is that
# of the HPO and users can get that from the HPO file and this should be
# provided in the constructor of metadata

default_versions = {
    'geno': '2022-03-05',
    'hgnc': '06/01/23',
    'omim': 'January 4, 2023',
    'mondo': '2023-09-12',
    'so': "2021-11-22"
}


class MetaData:
    """
    A representation of the MetaData element of the GA4GH Phenopacket Schema

    :param created_by: identifier (such as ORCID id) of the person who created this Phenopacket
    :type created_by: str
    :param pmid: PubMed identifier of the article from which the data for the phenopacket was taken, optional
    :type pmid: str
    :param pubmed_title: title of the article (if any), for use in the Resource section
    :type pubmed_title: str
    """

    def __init__(self, created_by, pmid=None, pubmed_title=None) -> None:
        """
        Constructor
        """
        self._created_by = created_by
        self._schema_version = "2.0"
        self._extref = None
        if pmid is not None and pubmed_title is not None:
            self.set_external_reference(pmid=pmid, pubmed_title=pubmed_title)
        self._resource_d = defaultdict(Resource)

    def default_versions_with_hpo(self, version, pmid=None, pubmed_title=None):
        """
        Add resources for HPO (with specified version), GENO, HGNC, and OMIM (with default versions)
        The HPO version can be easily obtained from the HpoParser using the get_version() function

        :param version: version of the Human Phenotype Ontology (HPO) used to create this phenopacket
        :type version: str
        :param pmid: PubMed identifier of the article from which the data for the phenopacket was taken, optional
        :type pmid: str
        :param pubmed_title: title of the article (if any), for use in the Resource section
        :type pubmed_title: str
        """
        self.geno()
        self.hgnc()
        self.omim()
        self.sequence_ontology()
        self.hpo(version=version)

    def hpo(self, version):
        """
        :param version: version of the Human Phenotype Ontology (HPO) used to create this phenopacket
        :type version: str
        """
        self._resource_d["hp"] = Resource(resource_id="hp",
                                        name="human phenotype ontology",
                                        namespace_prefix="HP",
                                        iriprefix="http://purl.obolibrary.org/obo/HP_",
                                        url="http://purl.obolibrary.org/obo/hp.owl",
                                        version=version)

    def geno(self, version=default_versions.get('geno')):
        """_summary_
        GENO is used for three terms: homozygous, heterozygous, hemizygous
        For this reason, we use a default version, since we assume these terms will not change.
        Args:
            version (str, optional): GENO version. Defaults to "2022-03-05".

        Returns:
            _type_: Resource object representing GENO
        """
        self._resource_d["geno"] = Resource(resource_id="geno",
                                            name="Genotype Ontology",
                                            namespace_prefix="GENO",
                                            iriprefix="http://purl.obolibrary.org/obo/GENO_",
                                            url="http://purl.obolibrary.org/obo/geno.owl",
                                            version=version)

    def hgnc(self, version=default_versions.get('hgnc')):
        self._resource_d["hgnc"] = Resource(resource_id="hgnc",
                                            name="HUGO Gene Nomenclature Committee",
                                            namespace_prefix="HGNC",
                                            iriprefix="https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/",
                                            url="https://www.genenames.org",
                                            version=version)

    def omim(self, version=default_versions.get('omim')):
        self._resource_d["omim"] = Resource(resource_id="omim",
                                            name="An Online Catalog of Human Genes and Genetic Disorders",
                                            namespace_prefix="OMIM",
                                            iriprefix="https://www.omim.org/entry/",
                                            url="https://www.omim.org",
                                            version=version)

    def mondo(self, version=default_versions.get('mondo')):
        """
        Add a resource for Mondo to the current MetaData object
        :param version: the Mondo version
        """
        self._resource_d["mondo"] = Resource(resource_id="mondo",
                                            name="Mondo Disease Ontology",
                                            namespace_prefix="MONDO",
                                            iriprefix="http://purl.obolibrary.org/obo/MONDO_",
                                            url="http://purl.obolibrary.org/obo/mondo.obo",
                                            version=version)

    def sequence_ontology(self, version=default_versions.get("so")):
        self._resource_d["so"] = Resource(resource_id="so",
                                            name="Sequence types and features ontology",
                                            namespace_prefix="SO",
                                            iriprefix="http://purl.obolibrary.org/obo/SO_",
                                            url="http://purl.obolibrary.org/obo/so.obo",
                                            version=version)

    def set_external_reference(self, pmid, pubmed_title) -> None:
        """
        Set the external reference for this phenopacket/individual to be the PubMed identifier and title of an article

        :param pmid: The PubMed identifier of the publication from which the data was derived
        :type pmid: str
        :param pubmed_title: The title of the publication
        :type pubmed_title: str
        """
        self._extref = PPKt.ExternalReference()
        self._extref.id = pmid
        pm = pmid.replace("PMID:", "")
        self._extref.reference = f"https://pubmed.ncbi.nlm.nih.gov/{pm}"
        self._extref.description = pubmed_title

    def get_pmid(self)->str:
        """
        :returns: The PubMed identifier
        :rtype: str:
        :raises ValueError: Throw an error if no PMID is available
        """
        if self._extref is not None:
            if self._extref.id.startswith("PMID"):
                return self._extref.id
            else:
                raise ValueError(f"Malformed PMID in external reference: {self._extref.id}")
        else:
            raise ValueError("Could not get PMID because MetaData._extref was None")


    def to_ga4gh(self):
        """
        Use a time stamp for the current instant
        :returns: A MetaData formated as a GA4GH Phenopacket Schema message
        :rtype: PPkt.MetaData
        """
        metadata = PPKt.MetaData()
        metadata.created_by = self._created_by
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        timestamp = protobuf.timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
        metadata.created.CopyFrom(timestamp)
        metadata.phenopacket_schema_version = self._schema_version
        for _, resource in self._resource_d.items():
            res = PPKt.Resource()
            res.id = resource.id
            res.name = resource.name
            res.namespace_prefix = resource.namespace_prefix
            res.iri_prefix = resource.iri_prefix
            res.url = resource.url
            res.version = resource.version
            metadata.resources.append(res)
        if self._extref is not None:
            metadata.external_references.append(self._extref)
        return metadata
