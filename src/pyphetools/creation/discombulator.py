import os
import pandas as pd
from collections import defaultdict
from .hpo_cr import HpoConceptRecognizer

class AnnotationRow:
    def __init__(self, idx) -> None:
        self._index = idx
        self._annot_list = list()
        self._annot_list.append(str(idx))

    def add_observed(self):
        self._annot_list.append("observed")

    def add_excluded(self):
        self._annot_list.append("excluded")

    def add_na(self):
        self._annot_list.append("na")

    def get_annot_lst(self):
        return self._annot_list

class Discombobulator:

    def __init__(self, hpo_cr:HpoConceptRecognizer) -> None:
        self._hpo_cr = hpo_cr

    def decode(self, df:pd.DataFrame, column:str, delim:str=",", assumeExcluded=False):
        if not column in df.columns:
            raise ValueError(f"could not find column {column} in dataframe")
        if not column in df.columns:
            raise ValueError(f"could not find column {column} in dataframe")
        index_to_hpo_set = defaultdict(set)
        label_to_id = dict()
        all_hpo_terms = set()
        ## First get list of all HPO terms used
        for idx, row in df.iterrows():
            idx = str(idx)
            contents = row[column]
            contents = str(contents) ## coerce to string in case empty
            hpo_term_list = self._hpo_cr.parse_cell(contents)
            for hterm in hpo_term_list:
                hpo_id = hterm.id
                label = hterm.label
                label_to_id[label] = hpo_id
                index_to_hpo_set[idx].add(label)
                all_hpo_terms.add(label)
        label_list = list()
        id_list = list()
        label_list.append("individual_id")
        id_list.append("str")

        # Now create dataframe with these annotations
        for h in all_hpo_terms:
            label_list.append(h)
            hpo_id = label_to_id.get(h)
            id_list.append(hpo_id)
        row_list = list()
        row_list.append(id_list)
        for hpo_list in index_to_hpo_set.values():
            for hpo in hpo_term_list:
                all_hpo_terms.add(hpo)
        hpo_annot_row = list()
        for idx, row in df.iterrows():
            idx = str(idx)
            if idx in index_to_hpo_set:
                observed_hpo_set = index_to_hpo_set.get(idx)
            else:
                observed_hpo_set = set() ## now terms parsed for this index

            arow = AnnotationRow(idx=idx)
            for hpo in label_list[1:]:
                if hpo in observed_hpo_set:
                    arow.add_observed()
                elif assumeExcluded:
                    arow.add_excluded()
                else:
                    arow.add_na()
            row_list.append(arow.get_annot_lst())
        # Create DataFrame
        df_out = pd.DataFrame(row_list, columns=label_list)
        return df_out
        
    def write(self, df:pd.DataFrame, column:str, delim:str=",", assumeExcluded=False):
        df = self.decode(df=df, column=column, delim=delim, assumeExcluded=assumeExcluded)
        fname = column.replace(" ", "_") + ".xlsx"
        df.to_excel(fname, index=False)
        print(f"Wrote Excel File with parsed columns to {fname}")

    