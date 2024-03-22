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
    :param disease_id: If provided, limit ingest to phenopackets with this disease ID
    :type disease_id: str
    """

    def __init__(self, indir, recursive:bool=False, disease_id:str=None) -> None:
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
                    if disease_id is not None:
                        if not PhenopacketIngestor.has_disease_id(ppkt=ppack, disease_id=disease_id):
                            continue
                    self._phenopackets.append(ppack)
        print(f"[pyphetools] Ingested {len(self._phenopackets)} GA4GH phenopackets.")

    @staticmethod
    def has_disease_id(ppkt:PPKt.Phenopacket, disease_id:str) -> bool:
        if len(ppkt.diseases) == 0:
            return False
        for disease in ppkt.diseases:
            if disease.HasField("term"):
                if disease_id == disease.term.id:
                    return True
        return False


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
