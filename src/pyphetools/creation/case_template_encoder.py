import abc
from typing import Dict, List
from pyphetools.creation.citation import Citation
from pyphetools.creation.constants import Constants
from pyphetools.creation.disease import Disease
from pyphetools.creation.metadata import MetaData
from pyphetools.creation.hp_term import HpTerm
from pyphetools.creation.individual import Individual
import os
import re
import pandas as pd
from google.protobuf.json_format import MessageToJson
import phenopackets as PPKt

class CellEncoder(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def encode(self, cell_contents):
        pass

    @abc.abstractmethod
    def is_data(self):
        pass

    @abc.abstractmethod
    def is_hpo(self):
        pass

class DataEncoder(CellEncoder):

    def __init__(self, h1:str, h2:str):
        super().__init__(name=h1)

    def encode(self, cell_contents):
        return str(cell_contents)

    def is_data(self):
        return True

    def is_hpo(self):
        return False

class HpoEncoder(CellEncoder):
    def __init__(self, h1:str, h2:str):
        super().__init__(name=h1)
        if h1.endswith(" "):
            raise ValueError(f"Error - HPO label ends with whitespace: \”{h1}\"")
        if not h2.startswith("HP:") or len(h2) != 10:
            raise ValueError(f"Error - Malformed HPO id: \”{h2}\"")
        self._hpo_label = h1
        self._hpo_id = h2

    def is_data(self):
        return False

    def is_hpo(self):
        return True

    def encode(self, cell_contents):
        cell_contents = str(cell_contents)
        if cell_contents == "observed":
            return HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)
        elif cell_contents == "excluded":
            return  HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)
        elif cell_contents.startswith("P"):
            # iso8601 age
            return  HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, onset=cell_contents)
        elif cell_contents == "na" or cell_contents == "nan" or len(cell_contents) == 0:
            return None
        else:
            raise ValueError(f"Could not parse HPO column cell_contents: \”{cell_contents}\"")

class NullEncoder(CellEncoder):
    def __init__(self, h1=None, h2=None):
        super().__init__(name="Begin of HPO column")

    def encode(self, cell_contents):
        return None

    def is_data(self):
        return False

    def is_hpo(self):
        return False

EXPECTED_HEADERS = {"PMID", "title", "individual_id", "Comment", "disease_id", "disease_label", "transcript",
                            "allele_1", "allele_2", "variant.comment", "age_of_onset", "sex"}

DATA_ITEMS = {"PMID", "title", "individual_id", "disease_id", "disease_label", "transcript",
                            "allele_1", "allele_2",  "age_of_onset", "sex"}




class CaseTemplateEncoder:

    HPO_VERSION = None

    def __init__(self, df, hpo_cr, created_by) -> None:
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"argment df must be pandas DataFrame but was {type(df)}")
        self._individuals = []
        header_1 = df.columns.values.tolist()
        header_2 = df.loc[0, :].values.tolist()
        if len(header_1) != len(header_2):
            # should never happen
            raise ValueError("headers are different lengths")
        self._n_columns = len(header_1)
        self._index_to_decoder = self._process_header(header_1, header_2)
        data_df = df.iloc[1:]
        self._is_biallelic = "allele_2" in header_1
        self._allele1_d = {}
        self._allele2_d = {}
        for _, row in data_df.iterrows():
            individual = self._parse_individual(row)
            self._individuals.append(individual)
            self._allele1_d[individual.id] = row["allele_1"]
            if self._is_biallelic:
                self._allele2_d[individual.id] = row["allele_2"]
        CaseTemplateEncoder.HPO_VERSION = hpo_cr.get_hpo_ontology().version
        self._created_by = created_by
        self._metadata_d = {}
        for i in self._individuals:
            cite = i._citation
            metadata = MetaData(created_by=created_by, citation=cite)
            metadata.default_versions_with_hpo(CaseTemplateEncoder.HPO_VERSION)
            self._metadata_d[i.id] = metadata

    def  _process_header(self, header_1, header_2) -> Dict[int, CellEncoder]:
        index_to_decoder_d = {}
        in_hpo_range = False
        for i in range(self._n_columns):
            h1 = header_1[i]
            h2 = header_2[i]
            if h1 == "HPO":
                in_hpo_range = True
                index_to_decoder_d[i] = NullEncoder()
                continue
            elif not in_hpo_range and h1 in EXPECTED_HEADERS:
                index_to_decoder_d[i] = DataEncoder(h1=h1, h2=h2)
                EXPECTED_HEADERS.remove(h1)
            elif in_hpo_range:
                index_to_decoder_d[i] = HpoEncoder(h1=h1, h2=h2)
        if not in_hpo_range:
            raise ValueError("Did not find HPO boundary column")
        print(f"Created encoders for {len(index_to_decoder_d)} fields")
        return index_to_decoder_d

    def _parse_individual(self, row):
        if not isinstance(row, pd.Series):
            raise ValueError(f"argment df must be pandas DSeriestaFrame but was {type(row)}")
        data = row.values.tolist()
        if len(data) != self._n_columns:
            # Should never happen
            raise ValueError(f"Divergent number of columns: header {self._n_columns} but data row {len(data)}: {data}")
        data_items = {}
        hpo_terms = list()
        for i in range(self._n_columns):
            encoder = self._index_to_decoder.get(i)
            cell_contents = data[i]
            if encoder is None:
                print(f"Encoder {i} was None for data {cell_contents}")
                continue
            if encoder.is_data() and encoder.name in DATA_ITEMS:
                data_items[encoder.name] = encoder.encode(cell_contents)
            elif encoder.is_hpo():
                hpoterm = encoder.encode(cell_contents)
                if hpoterm is not None:
                    hpo_terms.append(hpoterm)
        # Check we have all of the items we need
        for item in data_items.keys():
            if item not in DATA_ITEMS:
                raise ValueError(f"Unrecognized data item: \"{item}\"")
        #Note that allele_2 is optional
        if len(data_items) < len(DATA_ITEMS) - 1:
            raise ValueError(f"Insufficient data items: \"{data_items}\"")
        # If we get here, we can contruct an individual
        individual_id = data_items.get('individual_id')
        pmid = data_items.get("PMID")
        title = data_items.get("title")
        citation = Citation(pmid=pmid, title=title)
        sex = data_items.get("sex")
        if sex == "M":
            sex = Constants.MALE_SYMBOL
        elif sex == "F":
            sex = Constants.FEMALE_SYMBOL
        elif sex == "O":
            sex = Constants.OTHER_SEX_SYMBOL
        elif sex == "U":
            sex = Constants.UNKOWN_SEX_SYMBOL
        else:
            raise ValueError(f"Unrecognized sex symbol: {sex}")
        age = data_items.get("age")
        disease_id = data_items.get("disease_id")
        disease_label = data_items.get("disease_label")
        disease = Disease(disease_id=disease_id, disease_label=disease_label)
        return Individual(individual_id=individual_id,
                            citation=citation,
                            hpo_terms=hpo_terms,
                            sex=sex,
                            age=age,
                            disease=disease)

    def get_individuals(self):
        return self._individuals

    def get_allele1_d(self):
        return self._allele1_d

    def get_allele2_d(self):
        return self._allele2_d

    def _is_biallelic(self):
        return self._is_biallelic

    def get_metadata_d(self):
        return self._metadata_d

    def get_phenopackets(self):
        ppack_list = []
        for individual in self._individuals:
            cite = individual._citation
            metadata = MetaData(created_by=self._created_by, citation=cite)
            metadata.default_versions_with_hpo(CaseTemplateEncoder.HPO_VERSION)
            phenopckt = individual.to_ga4gh_phenopacket(metadata=metadata)
            ppack_list.append(phenopckt)
        return ppack_list



    def output_individuals_as_phenopackets(self, individual_list:List[Individual], outdir="phenopackets"):
        """write a list of Individual objects to file in GA4GH Phenopacket format
        Note that the individual_list needs to be passed to this object, because we expect that
        the QC code will have been used to cleanse the data of redundancies etc before output.
        We use the statefullness to keep track of the created_by argument from the constructor

        :param outdir: Path to output directory. Defaults to "phenopackets". Created if not exists.
        :type outdir: str
        """
        if os.path.isfile(outdir):
            raise ValueError(f"Attempt to create directory with name of existing file {outdir}")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        written = 0

        if self._created_by is None:
            created_by = 'pyphetools'
        else:
            created_by = self._created_by
        for individual in individual_list:
            cite = individual._citation
            metadata = MetaData(created_by=created_by, citation=cite)
            metadata.default_versions_with_hpo(CaseTemplateEncoder.HPO_VERSION)
            phenopckt = individual.to_ga4gh_phenopacket(metadata=metadata)
            json_string = MessageToJson(phenopckt)
            pmid = cite.pmid
            if pmid is None:
                fname = "phenopacket_" + individual.id
            else:
                pmid = pmid.replace(" ", "").replace(":", "_")
                fname = pmid + "_" + individual.id
            fname = re.sub('[^A-Za-z0-9_-]', '', fname)  # remove any illegal characters from filename
            fname = fname.replace(" ", "_") + ".json"
            outpth = os.path.join(outdir, fname)
            with open(outpth, "wt") as fh:
                fh.write(json_string)
                written += 1
        print(f"We output {written} GA4GH phenopackets to the directory {outdir}")
