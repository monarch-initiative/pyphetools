from datetime import datetime
from collections import defaultdict
import phenopackets 
from google import protobuf
import time



class Resource:
    def __init__(self, id, name, namespace_prefix, iriprefix, url, version) -> None:
        self._id = id
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
        
        
    
   

class MetaData:
    
    def __init__(self, created_by) -> None:
        self._created_by = created_by
        self._schema_version = "2.0"
        self._resource_d = defaultdict(Resource)
        
    def hpo(self, version):
        self._resource_d["hp"] = Resource(id="hp", 
                        name="human phenotype ontology",
                        namespace_prefix="HP",
                        iriprefix="http://purl.obolibrary.org/obo/HP_",
                        url="http://purl.obolibrary.org/obo/hp.owl",
                        version=version)

        
    def geno(self, version="2022-03-05"):
        """_summary_
        GENO is used for three terms: homozygous, heterozygous, hemizygous
        For this reason, we use a default version, since we assume these terms will not change.
        Args:
            version (str, optional): GENO version. Defaults to "2022-03-05".

        Returns:
            _type_: Resource object representing GENO
        """
        self._resource_d["geno"] = Resource(id="geno", 
                        name="Genotype Ontology",
                        namespace_prefix="GENO",
                        iriprefix="http://purl.obolibrary.org/obo/GENO_",
                        url="http://purl.obolibrary.org/obo/geno.owl",
                        version=version)
        
    def hgnc(self, version):
        self._resource_d["hgnc"] =  Resource(id="hgnc", 
                        name="HUGO Gene Nomenclature Committee",
                        namespace_prefix="HGNC",
                        iriprefix="https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/",
                        url="https://www.genenames.org",
                        version=version)
    
    
    def omim(self, version):
        self._resource_d["omim"] = Resource(id="omim", 
                        name="An Online Catalog of Human Genes and Genetic Disorders",
                        namespace_prefix="OMIM",
                        iriprefix="https://www.omim.org/entry/",
                        url="https://www.omim.org",
                        version=version)
    
    def mondo(self, version):
        self._resource_d["mondo"] = Resource(id="mondo", 
                        name="Mondo Disease Ontology",
                        namespace_prefix="MONDO",
                        iriprefix="http://purl.obolibrary.org/obo/MONDO_",
                        url="http://purl.obolibrary.org/obo/mondo.obo",
                        version=version)

    def to_ga4gh(self):
        """
        Use a time stamp for the current instant
        """
        metadata = phenopackets.MetaData()
        metadata.created_by = self._created_by
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        timestamp = protobuf.timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
        metadata.created.CopyFrom(timestamp)
        metadata.phenopacket_schema_version = self._schema_version
        for _, resource in self._resource_d.items():
            res = phenopackets.Resource()
            res.id = resource.id
            res.name = resource.name
            res.namespace_prefix = resource.namespace_prefix
            res.iri_prefix = resource.iri_prefix
            res.url = resource.url
            res.version = resource.version
            metadata.resources.append(res)
        return metadata



          

    
    
 
        
        
        

 
    
    
    
  