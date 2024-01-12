from collections import defaultdict
from .phenopacket_ingestor import PhenopacketIngestor
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



class PhenopacketCharts:

    def __init__(self, indir) -> None:
        ingestor = PhenopacketIngestor(indir=indir)
        simple_patient_list = list(ingestor.get_simple_patient_dictionary().values())
        self._disease_d = defaultdict(int)
        self._pmid_d = defaultdict(int)
        self._hpo_count_d = defaultdict(int) # total count
        self._term_count_d = defaultdict(int)

        for sp in simple_patient_list:
            self._disease_d[sp.get_disease()] += 1
            if sp.has_pmid():
                self._pmid_d[sp.get_pmid()] += 1
            self._hpo_count_d[sp.get_total_hpo_count()] += 1
            for hp in sp.get_observed_hpo_d().values():
                self._term_count_d[hp.label] += 1

    def disease_barchart(self):
        disease = []
        count = []
        for k,v in self._disease_d.items():
            disease.append(k)
            count.append(v)
        df = pd.DataFrame ({
            'Disease': disease,
            'Count': count
        })

        df = df.sort_values(by=['Count'])

        # Create horizontal bars
        ax = plt.barh(y=df.Disease, width=df.Count, height=0.2);

        # Add title
        plt.title('Diseases');
        return ax


    def pmid_barchart(self):
        pmid = []
        count = []
        for k,v in self._pmid_d.items():
            pmid.append(k)
            count.append(v)
        df = pd.DataFrame ({
            'PMID': pmid,
            'Count': count
        })

        df = df.sort_values(by=['Count'])

        # Create horizontal bars
        ax = plt.barh(y=df.PMID, width=df.Count, height=0.2);

        # Add title
        plt.title('Individuals per Citation');
        return ax


    def terms_per_phenopacket(self):
        count_vector = [x for x in self._hpo_count_d.values()]
        num_bins = np.max(count_vector)
        ax = plt.hist(count_vector,color ='green', alpha = 0.7, rwidth=0.85, bins=num_bins)
        plt.xlabel('HPO terms per individual')
        plt.ylabel('# Individuals')
        plt.title("Total HPO term counts per individual")
        return ax

    def most_common_hpo_terms(self, max_terms_to_show=10):
        sorted_terms = sorted(self._term_count_d.items(), key=lambda x:x[1], reverse=True)
        if len(sorted_terms) > max_terms_to_show:
            sorted_terms = sorted_terms[:max_terms_to_show]
        HPO = []
        count = []
        for st in sorted_terms:
            HPO.append(st[0])
            count.append(st[1])
        df = pd.DataFrame ({
            'HPO': HPO,
            'Count': count
        })

        df = df.sort_values(by=['Count'])

        # Create horizontal bars
        ax = plt.barh(y=df.HPO, width=df.Count, height=0.2);

        # Add title
        plt.title('Most common HPO annotations');
        return ax
