import abc
from typing import Dict, List
from pyphetools.creation.citation import Citation
from pyphetools.creation.constants import Constants
from pyphetools.creation.disease import Disease
from pyphetools.creation.hpo_cr import HpoConceptRecognizer
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
    """Convenience class to represent the header (two lines) of columns that represent fixed data in the template

    :param h1: contents of the first header line
    :type h1: str
    :param h2: contents of the second header line
    :type h2: str
    """
    def __init__(self, h1:str, h2:str):
        super().__init__(name=h1)

    def encode(self, cell_contents):
        return str(cell_contents)

    def is_data(self):
        return True

    def is_hpo(self):
        return False

class HpoEncoder(CellEncoder):
    """Convenience class to represent the header (two lines) of columns that represent HPO columns in the template

    :param h1: contents of the first header line
    :type h1: str
    :param h2: contents of the second header line
    :type h2: str
    """
    def __init__(self, h1:str, h2:str):
        super().__init__(name=h1)
        self._error = None
        self._hpo_label = None
        self._hpo_id = None
        if h1.endswith(" "):
            self._error = f"Error - HPO label ends with whitespace: \”{h1}\""
        elif h2.startswith("HP:") and len(h2) != 10:
            self._error = f"Error - Malformed HPO id: \”{h2}\" ({h1})"
        elif not h2.startswith("HP:"):
            self._error = f"Error - {h1} -- {h2}"
        else:
            self._hpo_label = h1
            self._hpo_id = h2

    def is_data(self):
        return False

    def is_hpo(self):
        """
        :returns: True iff this is an NPO column and there was no error
        :rtype: bool
        """
        return self._error is None

    def needs_attention(self):
        """
        :returns: True iff there was a problem with this column
        :rtype: bool
        """
        return self._error is not None

    def get_error(self):
        return self._error

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
    """Convenience class to represent a column that we do not use for encoding

    :param h1: contents of the first header line
    :type h1: str
    :param h2: contents of the second header line
    :type h2: str
    """
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
    """Class to encode data from user-provided Excel template.

    :param df: template table with clinical data
    :type df: pd.DataFrame
    :param hpo_cr: HpoConceptRecognizer for text mining
    :type hpo_cr: pyphetools.creation.HpoConceptRecognizer
    :param created_by: biocurator (typically, this should be an ORCID identifier)
    :type created_by: str
    """

    HPO_VERSION = None

    def __init__(self, df:pd.DataFrame, hpo_cr:HpoConceptRecognizer, created_by:str) -> None:
        """constructor
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"argument \"df\" must be pandas DataFrame but was {type(df)}")
        self._individuals = []
        self._errors = []
        header_1 = df.columns.values.tolist()
        header_2 = df.loc[0, :].values.tolist()
        if len(header_1) != len(header_2):
            # should never happen unless the template file is corrupted
            raise ValueError("headers are different lengths. Check template file for correctness.")
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

    def  _process_header(self, header_1:List, header_2:List) -> Dict[int, CellEncoder]:
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
            elif in_hpo_range:
                encoder = HpoEncoder(h1=h1, h2=h2)
                if encoder.needs_attention():
                    self._errors.append(encoder.get_error())
                    index_to_decoder_d[i] = NullEncoder()
                else:
                    index_to_decoder_d[i] = encoder
        if not in_hpo_range:
            raise ValueError("Did not find HPO boundary column")
        print(f"Created encoders for {len(index_to_decoder_d)} fields")
        return index_to_decoder_d

    def _parse_individual(self, row:pd.Series):
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

    def get_individuals(self) -> List[Individual]:
        return self._individuals

    def get_allele1_d(self)-> Dict[str,str]:
        return self._allele1_d

    def get_allele2_d(self)-> Dict[str,str]:
        return self._allele2_d

    def _is_biallelic(self) -> bool:
        return self._is_biallelic

    def get_metadata_d(self) -> Dict[str,MetaData]:
        return self._metadata_d

    def get_phenopackets(self) -> List[PPKt.Phenopacket]:
        ppack_list = []
        for individual in self._individuals:
            cite = individual._citation
            metadata = MetaData(created_by=self._created_by, citation=cite)
            metadata.default_versions_with_hpo(CaseTemplateEncoder.HPO_VERSION)
            phenopckt = individual.to_ga4gh_phenopacket(metadata=metadata)
            ppack_list.append(phenopckt)
        return ppack_list



    def output_individuals_as_phenopackets(self, individual_list:List[Individual], outdir="phenopackets") -> None:
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


    def to_summary(self) -> pd.DataFrame:
        """

        The table provides a summary of the table that was parsed from the input file. If there were errors, it
        provides enough feedback so that the user knows what needs to be fixed

        :returns: an table with status of parse
        :rtype: pd.DataFrame
        """
        n_error = 0
        items = []
        for e in self._errors:
            n_error += 1
            d = {'item': f"Error {n_error}", 'value': e}
            items.append(d)
        d = {'item': 'created by', 'value':self._created_by}
        items.append(d)
        d = {'item':'number of individuals', 'value': str(len(self._individuals))}
        items.append(d)
        n_hpo_columns = sum([1 for encoder in self._index_to_decoder.values() if encoder.is_hpo()])
        d = {'item':'number of HPO columns', 'value': str(n_hpo_columns)}
        items.append(d)
        return pd.DataFrame(items)



