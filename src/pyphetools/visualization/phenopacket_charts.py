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
        """barchart with y (height)=number of terms per phenopacket and x: number of phenopackets with that many terms
        """
        max_terms = max(self._hpo_count_d.keys())

        term_vector = []
        n_packet_vector = []
        for i in range(max_terms+1):
            n_packets = self._hpo_count_d.get(i, 0)
            term_vector.append(i)
            n_packet_vector.append(n_packets)
        ax = plt.bar(term_vector, n_packet_vector,color ='green', alpha = 0.7)
        # the following two lines cause the Y axis to show just integers for 20 or less
        max_n_individual = max(self._hpo_count_d.values())
        if max_n_individual < 21:
            yint = range(0, max_n_individual+1)
            plt.yticks(yint)
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
