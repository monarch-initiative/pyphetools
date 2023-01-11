import os
from collections import defaultdict
from .simple_patient import SimplePatient

class PhenopacketIngestor:
    
    def __init__(self, indir) -> None:
        if not os.path.isdir(indir):
            raise ValueError(f"indir argument {indir} must be directory!")
        self._indir = indir
        self._phenopackets = []
        self._patient_d = defaultdict(SimplePatient)
        for root, dirs, files in os.walk(indir):
            for file in files:
                if file.endswith(".json"):
                    self._phenopackets.append(file)
                    fullpath = os.path.join(indir, file)
                    patient = SimplePatient(phenopacket_file=fullpath)
                    phenopacket_id = patient.get_phenopacket_id()
                    self._patient_d[phenopacket_id] = patient

    def get_patient_dictionary(self):
        return self._patient_d
        