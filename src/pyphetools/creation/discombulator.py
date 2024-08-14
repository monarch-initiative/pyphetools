import pandas as pd
import typing
from collections import defaultdict
from .hpo_cr import HpoConceptRecognizer
from .hpo_parser import HpoParser

class AnnotationRow:
    """
    This class represents one row of the output file.
    """
    def __init__(self, idx) -> None:
        self._index = idx
        self._annot_list = list()
        self._annot_list.append(str(idx))

    def add_observed(self) -> None:
        self._annot_list.append("observed")

    def add_excluded(self) -> None:
        self._annot_list.append("excluded")

    def add_na(self) -> None:
        self._annot_list.append("na")

    def get_annot_lst(self) -> typing.List[str]:
        return self._annot_list

class Discombobulator:
    """
    Discombobulate a column of the original data, using text mining to find HPO terms and make one column for each identified HPO term in the output.
    In the following example, "Book2.xlsx" is an Excel file derived from an original publication. It has a column called "Cardiac defect", some of 
    whose cells contain items such as Ventricular septal defect, Atrial septal defect, Patent foramen ovale. Some of the cells contain codes (here, "na",
    and "UN") that indicate that no information is available (so we want to output "na"). The assumeExcluded argument means that if an observation
    was made (e.g., echocardiography), then we assume all items are excluded except those that are named in the cell. The decode method returns
    a pandas DataFrame that has columns that can be inspected and then added to the pyphetools Excel template once any necessary revisions have been made.
    The DataFrame will have one column for the patient identifier and one column for each of the identified HPO terms. Finally, the last column will be
    the original column that we can use to vet results.

        import pandas as pd
        df = pd.read_excel("../../Book2.xlsx")
        from pyphetools.creation import Discombobulator
        dc = Discombobulator(df=df, individual_id="individual column name")
        cardiac = dc.decode(column="Cardiac defect", trueNa={"na", "UN"}, assumeExcluded=True)
        cardiac.to_excel("cardiac.xlsx")

    """
    def __init__(self, 
                df:pd.DataFrame,
                individual_id:str,
                hpo_cr:HpoConceptRecognizer = None) -> None:
        if hpo_cr is not None:
            self._hpo_cr = hpo_cr
        else:
            parser = HpoParser()
            self._hpo_cr = parser.get_hpo_concept_recognizer()
        self._individual_id = individual_id
        self._df = df

    def decode(self,  
               column:str, 
               delim:str=",", 
               assumeExcluded=False, 
               trueNa:typing.Union[str,typing.Set[str]]="na") -> pd.DataFrame:
        """
        Discombobulate a column of the original data, using text mining to find HPO terms and make one column for each identified HPO term in the output.
        :param column: The name of the column to dsicombobulate
        :param delim: delimiter between items
        :assumeExcluded: Assume that if an item is not mentioned in a cell, then it was excluded. This can be justified if the column is about Echocardiography findings, for instance.
        :trueNa:  
        """
        if not column in self._df.columns:
            raise ValueError(f"could not find column {column} in dataframe")
        index_to_hpo_d = defaultdict(set)
        label_to_id = dict()
        all_hpo_terms = set()
        if isinstance(trueNa, str):
            self._true_na_set = set()
            self._true_na_set.add(trueNa)
        elif isinstance(trueNa, set):
            self._true_na_set = trueNa
        else:
            raise ValueError(f"trueNa argument must be string or set, but was {type(trueNa)}")
        ## First get list of all HPO terms used
        for idx, row in self._df.iterrows():
            idx = str(idx)
            contents = row[column]
            contents = str(contents) ## coerce to string in case empty
            hpo_term_list = self._hpo_cr.parse_cell(contents)
            for hterm in hpo_term_list:
                hpo_id = hterm.id
                label = hterm.label
                label_to_id[label] = hpo_id
                index_to_hpo_d[idx].add(label)
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
        for hpo_list in index_to_hpo_d.values():
            for hpo in hpo_term_list:
                all_hpo_terms.add(hpo)
        hpo_annot_row = list()
        for idx, row in self._df.iterrows():
            idx = str(idx)
            if idx in index_to_hpo_d:
                observed_hpo_set = index_to_hpo_d.get(idx)
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
        original_column = self._df[column]
        a = pd.Series(["Original"])
        new_column = pd.concat([a, original_column], axis=0, ignore_index=True)
        new_column_header = f"Original:{column}"
        df_out[new_column_header] = new_column
        df_out[new_column_header] = new_column
       

        # Now replace with na
        # List of columns to exclude
        for na_symbol in self._true_na_set:
            exclude_columns = ['individual_id', new_column_header]
            columns_to_change = df_out.columns.difference(exclude_columns)
            df_out.loc[df_out[new_column_header] == na_symbol, columns_to_change] = "na"
        # Now add back the original individual labels
        individual_column = self._df[self._individual_id]
        a = pd.Series(["Individual"])
        individual_column = pd.concat([a, individual_column], axis=0, ignore_index=True)
        df_out["original individual id"] = individual_column

        return df_out
        
    def write(self, df:pd.DataFrame, column:str, delim:str=",", assumeExcluded=False):
        df = self.decode(df=df, column=column, delim=delim, assumeExcluded=assumeExcluded)
        fname = column.replace(" ", "_") + ".xlsx"
        df.to_excel(fname, index=False)
        print(f"Wrote Excel File with parsed columns to {fname}")

    