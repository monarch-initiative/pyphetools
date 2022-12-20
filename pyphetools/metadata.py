from datetime import datetime
from collections import defaultdict
# Getting the current date and time


# getting the timestamp


class Resource:
    def __init__(self, id, name, namespace_prefix, iriprefix, url, version) -> None:
        self._id = id
        self._name = name
        self._namespace_prefix = namespace_prefix
        self._iriprefix = iriprefix
        self._url = name
        self._version = version
        
    def to_ga4gh(self):
        pass
        
        
    
   

class MetaData:
    
    def __init__(self, created_by, created=None) -> None:
        self._created_by = created_by
        if created is None:
            dt = datetime.now()
            self._created = dt # datetime.timestamp(dt)
        else:
            self._created = created
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
    
    
 
        
        
        

 
    
    
    
  