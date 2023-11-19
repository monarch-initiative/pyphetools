import os
from collections import defaultdict
import json
from google.protobuf.json_format import Parse
from .simple_patient import SimplePatient
from typing import Dict
import phenopackets as PPKt

class PhenopacketIngestor:
    """
    Ingest a collection of GA4GH Phenopacket objects from a directory

    :param indir: input directory
    :type indir: str
    :param recursive: Iff True, search subdirectorys for phenopackets
    :type recursive: bool, default False
    """

    def __init__(self, indir, recursive:bool=False) -> None:
        if not os.path.isdir(indir):
            raise ValueError(f"indir argument {indir} must be directory!")
        self._indir = indir
        self._phenopackets = []
        for file in os.listdir(indir):
            fname = os.path.join(indir, file)
            if fname.endswith(".json") and os.path.isfile(fname):
                with open(fname) as f:
                    data = f.read()
                    jsondata = json.loads(data)
                    ppack = Parse(json.dumps(jsondata), PPKt.Phenopacket())
                    self._phenopackets.append(ppack)
        print(f"[pyphetools] Ingested {len(self._phenopackets)} GA4GH phenopackets.")


    def get_simple_patient_dictionary(self) -> Dict:
        patient_d = defaultdict(SimplePatient)
        for ppack in self._phenopackets:
            patient = SimplePatient(ga4gh_phenopacket=ppack)
            patient_d[patient.get_subject_id()] = patient
        return patient_d


    def get_phenopacket_dictionary(self) -> Dict:
        patient_d = defaultdict(SimplePatient)
        for ppack in self._phenopackets:
            patient_d[ppack.id] = ppack
        return patient_d
