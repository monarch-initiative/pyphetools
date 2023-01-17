import os
import random
import time
import phenopackets
from phenopackets import Phenopacket
from google.protobuf.json_format import Parse
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import *
import json


class Downsampler:
    """
    This class flattens all observed terms into a set and also recorded variants, sex, identifier, and age
    The class purposefully disregards information about the time course in order to be able to count the 
    frequencies of HPO terms in groups
    """

    def __init__(self, phenopacket_file=None, ga4gh_phenopacket=None) -> None:
        if phenopacket_file is None and ga4gh_phenopacket is None:
            raise ValueError("Must pass either 'phenopacket_file' or 'ga4gh_phenopacket' argument")
        elif phenopacket_file is not None and ga4gh_phenopacket is not None:
            raise ValueError("Must pass only one of 'phenopacket_file' and 'ga4gh_phenopacket' arguments")
        elif phenopacket_file is not None:
            if not os.path.isfile(phenopacket_file):
                raise FileNotFoundError(f"Could not find phenopacket file at '{phenopacket_file}'") 
            with open(phenopacket_file) as f:
                data = f.read()
                jsondata = json.loads(data)
                self._phenopacket = Parse(json.dumps(jsondata), Phenopacket())
        else:
            # in this case, ga4gh_phenopacket cannot be None
            if str(type(ga4gh_phenopacket)) != "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":                   
                raise ValueError(f"phenopacket argument must be GA4GH Phenopacket Schema Phenopacket but was {type(ga4gh_phenopacket)}")
            else:
                self._phenopacket = ga4gh_phenopacket

    def downsample_positive_hpo_terms(self, k) -> Phenopacket:
        if not isinstance(k, int):
            raise ValueError(f"argument k must be an integer but was {type(k)}")
        observed_hpo_terms = []
        for pf in self._phenopacket.phenotypic_features:
            if pf.excluded:
                continue
            else:
                observed_hpo_terms.append(pf)
        downsampled = random.sample(observed_hpo_terms, k)
        print(f"We downsampled {len(observed_hpo_terms)} to {len(downsampled)} terms")
        downsampled_ppacket = Phenopacket()
        downsampled_ppacket.MergeFrom(self._phenopacket)
        downsampled_ppacket.phenotypic_features.clear()
        downsampled_ppacket.phenotypic_features.MergeFrom(downsampled)
        return downsampled_ppacket

    def write_downsampled_phenopacket(self, k, basename, outdir=None) -> None:
        downsampled_ppacket = self.downsample_positive_hpo_terms(k=k)
        json_string = MessageToJson(downsampled_ppacket)
        fname = basename + f"_{k}_{time.time()}_.json"
        if outdir is not None:
            outpth =  os.path.join(outdir, basename, fname)
        else:
            outpth = os.path.join(basename, fname)
        with open(outpth, "wt") as fh:
            fh.write(json_string)
            print(f"Wrote phenopacket to {outpth}")

        
        
    


