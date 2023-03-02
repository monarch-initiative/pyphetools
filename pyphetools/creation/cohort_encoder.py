import pandas as pd
from math import isnan
from typing import List
import os
import phenopackets
from google.protobuf.json_format import MessageToJson
import re

from .column_mapper import ColumnMapper
from .variant_column_mapper import VariantColumnMapper
from .hpo_cr import HpoConceptRecognizer
from .individual import Individual
from .metadata import MetaData

class CohortEncoder:
    
    def __init__(self, df, hpo_cr, column_mapper_d, individual_column_name, agemapper, sexmapper, metadata, variant_mapper=None, pmid=None):
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"df argument must be pandas data frame but was {type(df)}")
        if not isinstance(hpo_cr, HpoConceptRecognizer):
            raise ValueError(f"hpo_cr argument must be a HpoConceptRecognizer but was {type(hpo_cr)}")
        if not isinstance(column_mapper_d, dict):
            raise ValueError(f"column_mapper_d argument must be a dictionary but was {type(column_mapper_d)}")
        if not isinstance(individual_column_name, str):
            raise ValueError(f"individual_column_name argument must be a string but was {type(individual_column_name)}")
        if variant_mapper is not None and not isinstance(variant_mapper, VariantColumnMapper):
            raise ValueError(f"variant_mapper argument must be VariantColumnMapper but was {type(variant_mapper)}")
        if metadata is None:
            raise ValueError("Must pass a metadata object to constructor")
        # the following workaround is needed because isinstance gets confused about the two following classes
        elif str(type(metadata)) == "<class 'phenopackets.schema.v2.core.meta_data_pb2.MetaData'>":
            self._metadata = metadata
        elif str(type(metadata)) == "<class 'pyphetools.creation.metadata.MetaData'>":
            self._metadata = metadata.to_ga4gh()
        else:
            raise ValueError(F"Malformed metadata argument of type {type(metadata)}")
        self._df = df
        self._hpo_concept_recognizer = hpo_cr
        self._column_mapper_d = column_mapper_d
        self._id_column_name = individual_column_name
        #self._sex_column = individual_d.get('sex')
        self._age_mapper = agemapper
        self._sex_mapper = sexmapper
        self._disease_id = None
        self._disease_label = None
        self._variant_mapper = variant_mapper
        self._pmid = pmid
        
    def preview_dataframe(self):
        """
        Generate a dataframe with a preview of the parsed contents
        """
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        age_column_name = self._age_mapper.get_column_name()
        sex_column_name = self._sex_mapper.get_column_name()
        for index, row in df.iterrows():
            individual_id = row[self._id_column_name]
            age_cell_contents = row[age_column_name]
            age = self._age_mapper.map_cell(age_cell_contents)
            sex_cell_contents = row[sex_column_name]
            sex = self._sex_mapper.map_cell(sex_cell_contents)
            hpo_terms = []
            for column_name, column_mapper in self._column_mapper_d.items():
                cell_contents = row[column_name]
                ## Empty cells are often represented as float non-a-number by Pandas
                if isinstance(cell_contents, float) and isnan(cell_contents):
                    continue
                terms = column_mapper.map_cell(row[column_name])
                hpo_terms.extend(terms)
            hpo_string = "\n".join([h.to_string() for h in hpo_terms])
            d = {'id': individual_id,
                 'sex': sex,
                 'age': age,
                 'phenotypic features': hpo_string}
            individuals.append(d)
        df = pd.DataFrame(individuals)
        return df.set_index('id')
    
    def set_disease(self, disease_id, label):
        """_summary_
        If all patients in the cohort have the same disease we can set it with this method
        Args:
            id (str): disease identifier, e.g., OMIM:600123
            label (str): disease name
        """
        self._disease_id = disease_id
        self._disease_label = label
    
    
    def get_individuals(self, additional_hpo=None) -> List[Individual]:
        df = self._df.reset_index()  # make sure indexes pair with number of rows
        individuals = []
        age_column_name = self._age_mapper.get_column_name()
        sex_column_name = self._sex_mapper.get_column_name()
        if self._variant_mapper is None:
            variant_colname = None
        else:
            variant_colname = self._variant_mapper.get_column_name()
        count = 0
        for index, row in df.iterrows():
            individual_id = row[self._id_column_name]
            age_cell_contents = row[age_column_name]
            age = self._age_mapper.map_cell(age_cell_contents)
            sex_cell_contents = row[sex_column_name]
            sex = self._sex_mapper.map_cell(sex_cell_contents)
            if additional_hpo is None:
                hpo_terms = []
            else:
                hpo_terms = additional_hpo[count]
            for column_name, column_mapper in self._column_mapper_d.items():
                if column_name not in df.columns:
                    raise ValueError(f"Did not find column name '{column_name}' in dataframe -- check spelling!")
                cell_contents = row[column_name]
                ## Empty cells are often represented as float non-a-number by Pandas
                if isinstance(cell_contents, float) and isnan(cell_contents):
                    continue
                terms = column_mapper.map_cell(cell_contents)
                hpo_terms.extend(terms)
            if variant_colname is not None:
                variant_col = row[variant_colname]
                variant_list = self._variant_mapper.map_cell(variant_col)
            else:
                variant_list = []
            indi = Individual(individual_id=individual_id, sex=sex, age=age, hpo_terms=hpo_terms, variant_list=variant_list,
                              disease_id=self._disease_id, disease_label=self._disease_label)
            individuals.append(indi)
            count += 1
        return individuals

    def output_phenopackets(self, outdir="phenopackets"):
        """Output data about all individuals as GA4GH phenopackets

        Args:
            outdir (str): name of directory to write phenopackets (default: 'phenopackets')
        """
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        individual_list = self.get_individuals()
        written = 0
        for individual in individual_list:
            phenopckt = individual.to_ga4gh_phenopacket(metadata=self._metadata)
            json_string = MessageToJson(phenopckt)
            if self._pmid is None:
                fname = "phenopacket_" + individual.id + ".json"
            else:
                pmid = self._pmid.replace(" ", "").replace(":","_")
                fname = pmid + "_" + individual.id + ".json"
            fname = re.sub('[^\w_.)( -]', '', fname) #remove any illegal characters from filename
            fname = fname.replace(" ", "_")
            outpth = os.path.join(outdir, fname)
            with open(outpth, "wt") as fh:
                fh.write(json_string)
                written += 1
        print(f"Wrote {written} phenopackets to {outdir}")
