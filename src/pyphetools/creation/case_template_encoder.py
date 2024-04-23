import abc
from typing import Dict, List
from pyphetools.creation.citation import Citation
from pyphetools.creation.constants import Constants
from pyphetools.creation.disease import Disease
from pyphetools.creation.hpo_cr import HpoConceptRecognizer
from pyphetools.creation.metadata import MetaData
from pyphetools.creation.hp_term import HpTerm
from pyphetools.creation.individual import Individual
from pyphetools.creation.pyphetools_age import NoneAge, PyPheToolsAge
import os
import re
import pandas as pd
from google.protobuf.json_format import MessageToJson
import hpotk
import phenopackets as PPKt


# The following constants are identical with the constants used in the  Excel template
from pyphetools.pp.v202 import VitalStatus

AGE_OF_ONSET_FIELDNAME = "age_of_onset"
AGE_AT_LAST_ENCOUNTER_FIELDNAME = "age_at_last_encounter"

from enum import Enum


CellType = Enum('Celltype', ['DATA', 'HPO', 'NTR', 'MISC', 'NULL'])

class CellEncoder(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def columntype(self):
        pass

    @abc.abstractmethod
    def encode(self, cell_contents):
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

    def columntype(self):
        return CellType.DATA

class HpoEncoder(CellEncoder):
    """Convenience class to represent the header (two lines) of columns that represent HPO columns in the template

    :param h1: contents of the first header line
    :type h1: str
    :param h2: contents of the second header line
    :type h2: str
    """
    def __init__(self, h1:str, h2:str, ntr=False):
        super().__init__(name=h1)
        self._error = None
        self._hpo_label = None
        self._hpo_id = None
        self._is_ntr = ntr
        if h1.endswith(" "):
            self._error = f"Error - HPO label ends with whitespace: \”{h1}\""
        elif isinstance(h2, float):
            raise ValueError(f"second header was parsed as float which usually means it was empty: h1=\"{h1}\", h2=\"{h2}\"")
        elif h2.startswith("HP:") and len(h2) != 10:
            self._error = f"Error - Malformed HPO id: \”{h2}\" ({h1})"
        elif not h2.startswith("HP:"):
            self._error = f"Error: Did not recognize heaeder fields: - \"{h1}\" -- \"{h2}\""
        else:
            self._hpo_label = h1
            self._hpo_id = h2

    def is_data(self) -> bool:
        return False

    def columntype(self) -> "CellType":
        if self._is_ntr:
            return CellType.NTR
        else:
            return CellType.HPO

    def is_ntr(self) -> bool:
        """
        :returns: True if this is a new term request
        :rtype: bool
        """
        return self._is_ntr

    def needs_attention(self) -> bool:
        """
        :returns: True iff there was a problem with this column or if this is a new term request
        :rtype: bool
        """
        return self._is_ntr or self._error is not None

    def get_error(self) -> str:
        return self._error

    def encode(self, cell_contents) -> None:
        """
        Parses one cell from the template. Valid entries are observed, excluded, na, and ISO8601 age strings.
        Any other entry will lead to raising an Exception, probably the user entered something erroneous.
        """
        cell_contents = str(cell_contents)
        if cell_contents == "observed":
            return HpTerm(hpo_id=self._hpo_id, label=self._hpo_label)
        elif cell_contents == "excluded":
            return  HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)
        elif cell_contents == "na" or cell_contents == "nan" or len(cell_contents) == 0:
            return None
        elif len(cell_contents) > 0:
            try:
                onset = PyPheToolsAge.get_age(cell_contents)
                if onset.is_valid(): # valid OSO8601 age of onset
                    return HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, onset=onset)
            except Exception as parse_error:
                raise ValueError(f"Could not parse HPO column cell_contents: \”{str(parse_error)}\"")
            # if we cannot parse successfully, there is probably an error in the format. Drop down to end of function to warn user
        else:
            raise ValueError(f"Could not parse HPO column cell_contents: \”{cell_contents}\"")

class MiscEncoder(CellEncoder):
    """encode the optional Miscellaneous HPO encoder column, in which users can enter rarely annotated HPO terms as a list of semicolon-separated primary labels
    """
    def __init__(self, hpo_cr:HpoConceptRecognizer, h1=None, h2=None, ):
        super().__init__(name="Miscellaneous HPO column")
        self._hpo_cr = hpo_cr

    def encode(self, cell_contents):
        if isinstance(cell_contents, float):
            return []
        cell_contents = str(cell_contents)
        if len(cell_contents) == 0 or cell_contents == "nan":
            return []
        term_list = cell_contents.split(";")
        results = []
        for term_label in term_list:
            term = self._hpo_cr.get_term_from_label(term_label)
            results.append(term)
        return results

    def columntype(self):
        return CellType.MISC


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

    def columntype(self):
        return CellType.NULL

EXPECTED_HEADERS = {"PMID", "title", "individual_id", "comment", "disease_id", "disease_label",
                    "HGNC_id", "gene_symbol", "transcript", "allele_1", "allele_2",
                    "variant.comment", "age_of_onset", "age_at_last_encounter", "sex"}

DATA_ITEMS = {"PMID", "title", "individual_id", "disease_id", "disease_label", "HGNC_id",
                "gene_symbol", "transcript", "allele_1", "allele_2",  "age_of_onset",
                "age_at_last_encounter", "deceased", "sex"}

# note that the allele_2 field is option
REQUIRED_H1_FIELDS = ["PMID", "title", "individual_id",	"comment", "disease_id", "disease_label",
                    "HGNC_id", "gene_symbol", "transcript", "allele_1", "allele_2", "variant.comment", "age_of_onset", "age_at_last_encounter", "sex", "HPO"]
ALLELE_2_IDX = 8

REQUIRED_H2_FIELDS = ["CURIE", "str",	"str", "optional", "CURIE", "str", "CURIE",	"str",
                    "str","str","str","optional",  "age", "age", "M:F:O:U", "na"]

OPTIONAL_H1_FIELDS = REQUIRED_H1_FIELDS
OPTIONAL_H1_FIELDS.insert(14, "deceased")
OPTIONAL_H2_FIELDS = REQUIRED_H2_FIELDS
OPTIONAL_H2_FIELDS.insert(14, "yes/no/na")


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

    def __init__(self, df:pd.DataFrame, hpo_cr:HpoConceptRecognizer, created_by:str, hpo_ontology:hpotk.MinimalOntology) -> None:
        """constructor
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"argument \"df\" must be pandas DataFrame but was {type(df)}")
        self._individuals = []
        self._errors = []
        self._ntr_set = set()
        header_1 = df.columns.values.tolist()
        header_2 = df.loc[0, :].values.tolist()
        if len(header_1) != len(header_2):
            # should never happen unless the template file is corrupted
            raise ValueError("headers are different lengths. Check template file for correctness.")
        # check headers are well formed
        idx = 0
        ## The deceased field is optional
        if "deceased" in header_1:
            required_h1 = OPTIONAL_H1_FIELDS
            required_h2 = OPTIONAL_H2_FIELDS
        else:
            required_h1 = REQUIRED_H1_FIELDS
            required_h2 = REQUIRED_H2_FIELDS
        for i in range(len(required_h1)):
            if idx == ALLELE_2_IDX and header_1[idx] != required_h1[idx]:
                idx += 1 # skip optional index
            if header_1[idx] != required_h1[idx]:
                raise ValueError(f"Malformed header 1 field at index {idx}. Expected \"{required_h1[idx]}\" but got \"{header_1[idx]}\"")
            if header_2[idx] != required_h2[idx]:
                raise ValueError(f"Malformed header 2 field at index {idx}. Expected \"{required_h2[idx]}\" but got \"{header_2[idx]}\"")
        self._header_fields_1 = header_1
        self._n_columns = len(header_1)
        self._index_to_decoder = self._process_header(header_1=header_1, header_2=header_2, hpo_cr=hpo_cr)
        data_df = df.iloc[1:]
        self._check_for_duplicate_individual_ids(data_df)
        self._is_biallelic = "allele_2" in header_1
        self._allele1_d = {}
        self._allele2_d = {}
        for _, row in data_df.iterrows():
            individual = self._parse_individual(row)
            self._individuals.append(individual)
            self._allele1_d[individual.id] = row["allele_1"]
            if self._is_biallelic:
                self._allele2_d[individual.id] = row["allele_2"]
        CaseTemplateEncoder.HPO_VERSION = hpo_ontology.version
        self._created_by = created_by
        self._metadata_d = {}
        for i in self._individuals:
            cite = i._citation
            metadata = MetaData(created_by=created_by, citation=cite)
            metadata.default_versions_with_hpo(CaseTemplateEncoder.HPO_VERSION)
            self._metadata_d[i.id] = metadata

    def  _process_header(self, header_1:List, header_2:List, hpo_cr:HpoConceptRecognizer) -> Dict[int, CellEncoder]:
        index_to_decoder_d = {}
        in_hpo_range = False
        for i in range(self._n_columns):
            h1 = header_1[i]
            h2 = header_2[i]
            if isinstance(h1, float) or len(h1) == 0:
                raise ValueError(f"Error: Empty column header at column {i}")

            if h1 == "HPO":
                in_hpo_range = True
                index_to_decoder_d[i] = NullEncoder()
                continue
            if h1 == "Miscellaneous":
                index_to_decoder_d[i] = MiscEncoder(h1=h1, h2=h2, hpo_cr=hpo_cr)
            elif not in_hpo_range:
                if h1 in EXPECTED_HEADERS:
                    index_to_decoder_d[i] = DataEncoder(h1=h1, h2=h2)
                elif h1 == "deceased":
                    index_to_decoder_d[i] = DataEncoder(h1=h1, h2=h2)
                else:
                    raise ValueError(f"Malformed template header at column {i}: \"{h1}\"")
            elif in_hpo_range:
                ntr =  h2 == "NTR"
                encoder = HpoEncoder(h1=h1, h2=h2, ntr=ntr)
                if ntr:
                    self._ntr_set.add(h1)
                    index_to_decoder_d[i] = encoder
                elif encoder.needs_attention():
                    self._errors.append(encoder.get_error())
                    index_to_decoder_d[i] = NullEncoder()
                else:
                    index_to_decoder_d[i] = encoder
        if not in_hpo_range:
            raise ValueError("Did not find HPO boundary column")
        print(f"Created encoders for {len(index_to_decoder_d)} fields")
        if len(self._ntr_set) > 0:
            print("[WARNING] Template contains new term requests (NTR). These columns will be ignored until they are replaced with HPO terms")
            for ntr in self._ntr_set:
                print("\tNTR: ", ntr)
        if len(self._errors) > 0:
            for e in self._errors:
                print(f"ERROR: {e}")
        return index_to_decoder_d

    def _check_for_duplicate_individual_ids(self, df:pd.DataFrame) -> None:
        """Check that no two individuals in the dataframe have the same identifier
        Duplicate identifiers can lead to other errors in the code
        An identifier is made from the combination of PMID and individual_id and must be unique
        If there is one or mure duplicates, this function will throw a value error.
        """
        if not "individual_id" in df.columns:
            raise ValueError(f"Malformed template headers - could not find column \"individual_id\"")
        if not "PMID" in df.columns:
            raise ValueError(f"Malformed template headers - could not find column \"individual_id\"")
        seen_ids = set()
        errors = list()
        for _, row in df.iterrows():
            individual_id = row["individual_id"]
            pmid = row["PMID"]
            composite_id = f"{pmid}_{individual_id}"
            if composite_id in seen_ids:
                errors.append(f"Duplicate identifier: {composite_id}")
            else:
                seen_ids.add(composite_id)
        if len(errors) > 0:
            err_str = "\n".join(errors)
            raise ValueError(err_str)
        # else, all is OK, no duplicate ids

    def _parse_individual(self, row:pd.Series):
        if not isinstance(row, pd.Series):
            raise ValueError(f"argument df must be pandas DSeriestaFrame but was {type(row)}")
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
                print(f"Encoder {i} was None for data \"{cell_contents}\"")
                self._debug_row(i, row)
                raise ValueError(f"Encoder {i} was None for data \"{cell_contents}\"")
            elif encoder.columntype == CellType.NTR:
                continue ## cannot be use yet because new term request.
            encoder_type = encoder.columntype()
            if encoder_type == CellType.DATA and encoder.name in DATA_ITEMS:
                data_items[encoder.name] = encoder.encode(cell_contents)
            elif encoder_type == CellType.HPO:
                try:
                    hpoterm = encoder.encode(cell_contents)
                    if hpoterm is not None:
                        hpo_terms.append(hpoterm)
                except Exception as hpo_parse_exception:
                    errr = f"Could not parse contents of HPO column {encoder.name}: {cell_contents} because of {str(hpo_parse_exception)}"
                    print(errr)
                    raise ValueError(errr)
            elif encoder_type == CellType.MISC:
                term_list = encoder.encode(cell_contents=cell_contents)
                for trm in term_list:
                    hpo_terms.append(trm)
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
            sex = Constants.UNKNOWN_SEX_SYMBOL
        else:
            raise ValueError(f"Unrecognized sex symbol: {sex} for individual \"{individual_id}\"")
        onset_age = data_items.get(AGE_OF_ONSET_FIELDNAME)
        if onset_age is not None and isinstance(onset_age, str):
            onset_age = PyPheToolsAge.get_age(onset_age)
        else:
            onset_age = NoneAge("na")
        encounter_age = data_items.get(AGE_AT_LAST_ENCOUNTER_FIELDNAME)
        if encounter_age is not None and isinstance(encounter_age, str):
            encounter_age = PyPheToolsAge.get_age(encounter_age)
        else:
            encounter_age = NoneAge("na")
        vitStat = None
        if "deceased" in data_items:
            decsd = data_items.get("deceased")
            if encounter_age.is_valid():
                timeelem = encounter_age.to_ga4gh_time_element()
                vitStat = VitalStatus(status=VitalStatus.Status.DECEASED, time_of_death=timeelem)
            else:
                vitStat = VitalStatus(status=VitalStatus.Status.DECEASED)
        disease_id = data_items.get("disease_id")
        disease_label = data_items.get("disease_label")
        # common error -- e.g. PMID: 3000312 or OMIM: 600123 (whitespace after colon)
        for item in [pmid, disease_id]:
            if " " in item:
                raise ValueError(f"Found illegal whitespace in {item}. Please remove it and try again")
        disease = Disease(disease_id=disease_id, disease_label=disease_label)
        return Individual(individual_id=individual_id,
                            citation=citation,
                            hpo_terms=hpo_terms,
                            sex=sex,
                            age_of_onset=onset_age,
                            age_at_last_encounter=encounter_age,
                            vital_status=vitStat,
                            disease=disease)

    def _debug_row(self, target_idx:int, row:pd.Series):
        row_items = list(row)
        for j in range(len(row_items)):
            hdr = self._header_fields_1[j]
            if j == target_idx:
                print(f"[{j}] *** {hdr}={row_items[j]}  ***")
            else:
                print(f"[{j}] {hdr}={row_items[j]}")

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



    def _transform_individuals_to_phenopackets(self, individual_list:List[Individual]):
        """Create one phenopacket for each of the individuals

        :param individual_list: List of individual objects
        :type individual_list:List[Individual]
        :returns: list of corresponding phenopackets
        :rtype: List[PPKt.Phenopacket]
        """
        ppkt_list = list()
        if self._created_by is None:
            created_by = 'pyphetools'
        else:
            created_by = self._created_by
        for individual in individual_list:
            cite = individual._citation
            metadata = MetaData(created_by=created_by, citation=cite)
            metadata.default_versions_with_hpo(CaseTemplateEncoder.HPO_VERSION)
            phenopckt = individual.to_ga4gh_phenopacket(metadata=metadata)
            ppkt_list.append(phenopckt)
        return ppkt_list

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


    def print_individuals_as_phenopackets(self, individual_list:List[Individual]) -> None:
        """Function designed to show all phenopackets in a notebook for Q/C
        :param individual_list: List of individual objects
        :type individual_list:List[Individual]
        """
        ppkt_list = self._transform_individuals_to_phenopackets(individual_list)
        for ppkt in ppkt_list:
            json_string = MessageToJson(ppkt)
            print("####")
            print(json_string)


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



