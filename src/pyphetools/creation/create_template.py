import os
import typing

import pandas as pd
from collections import defaultdict
from .hpo_parser  import HpoParser
from .hp_term import HpTerm
from typing import List
import hpotk
from .case_template_encoder import REQUIRED_H1_FIELDS, REQUIRED_H2_FIELDS

class TemplateCreator:

    def __init__(
            self,
            hp_json: typing.Optional[str] = None,
            hp_cr_index: typing.Optional[str] = None,
    ) -> None:
        if hp_json is None:
            parser = HpoParser()
        elif not os.path.isfile(hp_json):
            raise FileNotFoundError(f"Could not find hp.json file at {hp_json}")
        else:
            parser = HpoParser(hpo_json_file=hp_json)
        if hp_cr_index is not None:
            if not os.path.isfile(hp_cr_index):
                raise FileNotFoundError(f"Could not find the FastHPOCR index file at {hp_cr_index}")

        self._hpo_cr = parser.get_hpo_concept_recognizer(hp_cr_index=hp_cr_index)
        self._hpo_ontology = parser.get_ontology()
        self._all_added_hp_term_set = set()



    def add_seed_terms(self, text:str) -> None:
        """add HPO terms that will be used in the template
        The function will use text mining to extract terms from the text argument, which
        can have any desired format (e.g., a paragraph from a publication or
        a list of HPO term labels, one per line, etc.)

        :param text: free text that contains HPO term labels to be mined
        :type text: str
        """
        for line in text.split("\n"):
            hpo_term_list = self._hpo_cr.parse_cell(line)
            for hpt in hpo_term_list:
                self._all_added_hp_term_set.add(hpt)


    def arrange_terms(self) -> List[hpotk.model.TermId]:
        hp_term_list = list()
        ## Arrange hp_terms so that all terms that belong to a given top level term go together
        PHENO_ROOT_TERM_ID = "HP:0000118"
        top_level_term_ids = self._hpo_ontology.graph.get_children(PHENO_ROOT_TERM_ID, True)
        top_level_term_ids = list(top_level_term_ids)
        top_level_d = defaultdict(list)
        for hpt in self._all_added_hp_term_set:
            found= False
            for tlt in top_level_term_ids:
                if self._hpo_ontology.graph.is_descendant_of(hpt.id,tlt):
                    found = True
                    top_level_d[tlt].append(hpt)
                    break
            if not found:
                raise ValueError(f"Could not find top level ancestor of {hpt.label}")
        # Now the terms can be arrange by top level ancestor, which will make it easier to enter
        # in the Excel sheet
        for tlt, hpt_list in top_level_d.items():
            hp_term_list.extend(hpt_list)
        print(f"[INFO] Add {len(hp_term_list)} HPO terms to template.")
        return hp_term_list


    def create_template(self, disease_id:str, disease_label:str, HGNC_id:str, gene_symbol:str, transcript:str):
        """Create an Excel file that can be used to enter data as a pyphetools template

        :param disease_id: an OMIM, MONDO, or other similar CURIE identifier
        :param disease_label: the corresponding name
        :param HGNC_id: HUGO Gene Nomenclattre Committee identifier, e.g., HGNC:3603
        :param gene_symbol: corresponding gene symbol, e.g., FBN1
        :transcript: transcript to be used for the HVGC nomenclature. Must be refseq with version number
        """
        H1_Headers = REQUIRED_H1_FIELDS
        H2_Headers = REQUIRED_H2_FIELDS
        if len(H1_Headers) != len(H2_Headers):
            raise ValueError("Header lists must have same length")
        EMPTY_STRING = ""
        hp_term_list = self.arrange_terms()
        for hpt in hp_term_list:
            H1_Headers.append(hpt.label)
            H2_Headers.append(hpt.id)
        df = pd.DataFrame(columns=H1_Headers)
        new_row = dict()
        for i in range(len(H1_Headers)):
            new_row[H1_Headers[i]] = H2_Headers[i]
        df.loc[len(df)] = new_row
        # add 10 rows with the constant data columns
        for i in range(10):
            new_row = dict()
            for i in range(len(H1_Headers)):
                header_field = H1_Headers[i]
                if header_field == "disease_id":
                    new_row[header_field] = disease_id
                elif header_field == "disease_label":
                    new_row[header_field] = disease_label
                elif header_field == "HGNC_id":
                    new_row[header_field] = HGNC_id
                elif header_field == "gene_symbol":
                    new_row[header_field] = gene_symbol
                elif header_field == "HGNC_id":
                    new_row[header_field] = HGNC_id
                elif header_field == "transcript":
                    new_row[header_field] = transcript
                elif header_field == "HPO":
                    new_row[header_field] = "na"
                else:
                    new_row[header_field] = EMPTY_STRING
            df.loc[len(df)] = new_row
        ## Output as excel
        fname = disease_id.replace(":", "_") + "_individuals.xlsx"
        if os.path.isfile(fname):
            raise FileExistsError(f"Excel file '{fname}' already exists.")
        df.to_excel(fname, index=False)
        print(f"Wrote Excel pyphetools template file to {fname}")

    def create_from_phenopacket(self, ppkt):
        """
        create pyphetools templates from an individual phenopacket.
        This function is intended to accelerate the process of converting the LIRICAL phenopackets
        to our current format and generally should not be used for new cases
        """
        id_to_observed = set()
        id_to_excluded = set()

        for pf in ppkt.phenotypic_features:
            hpt = HpTerm(hpo_id=pf.type.id, label=pf.type.label)
            self._all_added_hp_term_set.add(hpt)
            if pf.excluded:
                id_to_excluded.add(pf.type.label)
            else:
                id_to_observed.add(pf.type.label)
        H1_Headers = REQUIRED_H1_FIELDS
        H2_Headers = REQUIRED_H2_FIELDS
        if len(H1_Headers) != len(H2_Headers):
            raise ValueError("Header lists must have same length")
        EMPTY_STRING = ""
        hp_term_list = self.arrange_terms()
        for hpt in hp_term_list:
            H1_Headers.append(hpt.label)
            H2_Headers.append(hpt.id)
        df = pd.DataFrame(columns=H1_Headers)
        new_row = dict()
        for i in range(len(H1_Headers)):
            new_row[H1_Headers[i]] = H2_Headers[i]
        df.loc[len(df)] = new_row
        # add one row with some of the data from the phenopakcet
        new_row = dict()
        for i in range(len(H1_Headers)):
            header_field = H1_Headers[i]
            if header_field == "HPO":
                new_row[header_field] = "na"
            elif header_field in id_to_observed:
                new_row[header_field] = "observed"
            elif header_field in id_to_excluded:
                new_row[header_field] = "excluded"
            else:
                new_row[header_field] = "?"
        df.loc[len(df)] = new_row
        ## Output as excel
        ppkt_id = "".join(e for e in ppkt.id if e.isalnum())
        fname = ppkt_id + "_phenopacket_template.xlsx"
        df.to_excel(fname, index=False)
        print(f"Wrote excel pyphetools template file to {fname}")
