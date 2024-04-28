import os, sys, re
import pandas as pd
from collections import defaultdict
import typing
import phenopackets as PPKt


class TemplateImporter:
    """Convenience class to streamline the process of createing phenopackets
    The class transforms data from an Excel file into phenopackets, and optionally creates
    the corresponding HPOA file.
    """

    ORCID_regex = r"^\d{4}-\d{4}-\d{4}-\d{4}$"

    def __init__(self,template:str,
                created_by:str,
                hp_json:str=None) -> None:
        """Constructor

        :param template: path to Excel template file
        :type template: str
        :param hp_json: path to hp.json file
        :type hp_json: str
        :param created_by: ORCID identifier of the biocurator
        :type created_by: str
        """
        if "ORCID" in created_by.upper():
            created_by = created_by.replace("ORCID:", "")
        match = re.search(TemplateImporter.ORCID_regex, created_by)
        if not match:
            if "http" in created_by:
                raise ValueError(f"Invalid ORCID {created_by} -- do not use URL! Only the ORCID number")
            else:
                raise ValueError(f"Invalid ORCID {created_by}")
        self._created_by = f"ORCID:{created_by}"
        if not os.path.isfile(template):
            raise FileNotFoundError(f"Could not find Excel template at {template}")
        if hp_json is not None and not os.path.isfile(hp_json):
            raise FileNotFoundError(f"Could not find hp.json file at {hp_json}")
        self._template = template
        self._hp_json = hp_json

    @staticmethod
    def _get_data_from_template(df:pd.DataFrame) -> typing.Tuple[str,str,str,str,str]:
        """Check that the template (dataframe) has the columns
        "HGNC_id", "gene_symbol", "transcript",
        If each row has the same value for these columns, then the template is valid
        and we can proceed.

        :param df: the template with data about a cohort
        :type df: pd.DataFrame
        :returns: Tuple of 5 strings-disease_id, disease_label, HGNC_id, gene_symbol, transcript
        :rtype: typing.Tuple[str,str,str,str,str]
        """
        contents_d = defaultdict(set)
        for item in ["disease_id", "disease_label", "HGNC_id", "gene_symbol", "transcript"]:
            if item not in df.columns:
                raise ValueError(f"Invalid template -- could not find the \"{item}\" column")
        ## We need to skip the first row (second row of excel file), which has the datatypes
        for _, row in df.iloc[1: , :].iterrows():
            contents_d["disease_id"].add(row["disease_id"])
            contents_d["disease_label"].add(row["disease_label"])
            contents_d["HGNC_id"].add(row["HGNC_id"])
            contents_d["gene_symbol"].add(row["gene_symbol"])
            contents_d["transcript"].add(row["transcript"])
        for item in ["HGNC_id", "gene_symbol", "transcript"]:
            if len(contents_d.get(item)) != 1:
                # should never happen unless the template is improperly formated
                all_items = "; ".join(contents_d.get(item))
                raise ValueError(f"invalid item set for {item}: {all_items}")
        # If we get here, the data are complete and consistent
        # Note that the values of contents_d are sets of strings.
        # We also know there is only one element per set, which we get with "pop"
        disease_id = contents_d.get("disease_id").pop()
        disease_label = contents_d.get("disease_label").pop()
        HGNC_id = contents_d.get("HGNC_id").pop()
        gene_symbol = contents_d.get("gene_symbol").pop()
        transcript = contents_d.get("transcript").pop()
        return disease_id, disease_label, HGNC_id, gene_symbol, transcript

    @staticmethod
    def _get_allelic_requirement(df:pd.DataFrame):
        """Determine allelic requirement
        Note that we always expect the column allele_1 to have content.
        If each row of allele_2 is "na", then the allelic requirement is MONO_ALLELIC
        If each row of allele_2 is not "na" and contains a variant string, then the
        requirement is BI_ALLELIC.
        Mixtures of MONO and BI ALLELIC are not allowed by this script, and more involved
        Python scripts will be needed to ingest the data.

        :param df: DataFrame with cohort data
        :type df: pd.DataFrame
        """
        from pyphetools.creation import AllelicRequirement
        total_row_count = 0
        total_allele_2_na_count = 0
        for _, row in df.iloc[1: , :].iterrows():
            a1 = row["allele_1"]
            a2 = row["allele_2"]
            if a1 == "na":
                raise ValueError(f"Invalid row with na allele_1: {row}")
            if a2 != "na":
                total_allele_2_na_count += 1
            elif len(a2) == 0:
                raise ValueError(f"Invalid row with empty allele_2: {row}")
            total_row_count += 1
        if total_allele_2_na_count == 0:
            return AllelicRequirement.MONO_ALLELIC
        elif total_allele_2_na_count == total_row_count:
            return AllelicRequirement.BI_ALLELIC
        else:
            raise ValueError(f"Error: {total_allele_2_na_count} rows with two alleles but {total_row_count} total rows")



    def import_phenopackets_from_template(self,
                                          deletions:typing.Set[str]=set(),
                                        duplications:typing.Set[str]=set(),
                                        inversions:typing.Set[str]=set(),
                                        hemizygous:bool=False):
        """Import the data from an Excel template and create a collection of Phenopackets

        Note that things will be completely automatic if the template just has HGNC encoding variants
        If there are structural variants, we need to encode them by hand by passing them as
        elements of the sets of deletions, duplications, or inversions. Note that other Structural Variant types may be added later as required.
        :param deletions: Strings (identical to entries in the templates) that represent deletions.
        :type deletions: (typing.Set[str], optional
        :param duplications: Strings (identical to entries in the templates) that represent duplications.
        :type duplications: (typing.Set[str], optional
        :param inversions: Strings (identical to entries in the templates) that represent inversions.
        :type inversions: (typing.Set[str], optional
        :param hemizygous: Set this to true for X-chromosomal recessive conditions in which the genotype of affected males is hemizygous
        :type hemizygous: bool
        :returns: tuple with individual list and CohortValidator that optionally can be used to display in a notebook
        :rtype: typing.Tuple[typing.List[pyphetools.creation.Individual], pyphetools.validation.CohortValidator]
        """
        from pyphetools.creation  import HpoParser
        from pyphetools.creation import CaseTemplateEncoder
        from pyphetools.creation import VariantManager
        from pyphetools.validation import CohortValidator
        parser = HpoParser(hpo_json_file=self._hp_json)
        hpo_cr = parser.get_hpo_concept_recognizer()
        hpo_ontology = parser.get_ontology()
        print(f"HPO version {hpo_ontology.version}")
        df = pd.read_excel(self._template)
        encoder = CaseTemplateEncoder(df=df, hpo_cr=hpo_cr, created_by=self._created_by, hpo_ontology=hpo_ontology)
        individuals = encoder.get_individuals()
        disease_id, disease_label, HGNC_id, gene_symbol, transcript = TemplateImporter._get_data_from_template(df)
        print(f"Importing {disease_id}, {disease_label}, {HGNC_id}, {gene_symbol},  {transcript}")
        vman = VariantManager(df=df, individual_column_name="individual_id",
                                allele_1_column_name="allele_1",
                                allele_2_column_name="allele_2",
                                gene_id=HGNC_id,
                                gene_symbol=gene_symbol,
                                transcript=transcript)
        if len(deletions) > 0:
            vman.code_as_chromosomal_deletion(deletions)
        if len(duplications) > 0:
            vman.code_as_chromosomal_duplication(duplications)
        if len(inversions) > 0:
            vman.code_as_chromosomal_inversion(inversions)
        if vman.has_unmapped_alleles():
            mapped = vman.get_mapped_allele_count()
            print(f"We were able to map {mapped} alleles.")
            print("The following alleles could not be mapped. Either there is an error or the variants are structural and require special treatment (see documentation)")
            for uma in vman.get_unmapped_alleles():
                if uma.startswith("c."):
                    print(f"- {transcript}:{uma}")
                else:
                    print(f"- {uma} (may require coding as structural variant)")
            print("Fix this error and then try again!")
            sys.exit(1)
        vman.add_variants_to_individuals(individuals, hemizygous=hemizygous)
        all_req = TemplateImporter._get_allelic_requirement(df)
        cvalidator = CohortValidator(cohort=individuals, ontology=hpo_ontology, min_hpo=1, allelic_requirement=all_req)
        if cvalidator.n_removed_individuals() > 0:
            print(f"Removed {cvalidator.n_removed_individuals()} individuals with unfixable errors")
        ef_individuals = cvalidator.get_error_free_individual_list()
        encoder.output_individuals_as_phenopackets(individual_list=ef_individuals)
        return individuals, cvalidator



    @staticmethod
    def check_disease_entries(ppkt_list:typing.List[PPKt.Phenopacket]) -> None:
        disease_count_d = defaultdict(int)
        for ppkt in ppkt_list:
            # Each phenopacket must have one disease
            if len(ppkt.diseases) == 0:
                error_msg = f"Phenopackt {ppkt.id} did not have a disease entry."
                print(error_msg)
                raise ValueError(error_msg)
            elif len(ppkt.diseases) > 1:
                # multiple disease per phenopacket are not allowed in this script
                diseases = ppkt.diseases
                disease_str = "; ".join([f"{d.term.label} ({d.term.id})" for d in diseases])
                error_msg = f"Phenopackt {ppkt.id} had multiple disease entries: {disease_str}."
                print(error_msg)
                raise ValueError(error_msg)
            d = ppkt.diseases[0]
            d_str = f"{d.term.label} ({d.term.id})"
            disease_count_d[d_str] += 1
        # The cohort is only allowed to have one and the same disease
        if len(disease_count_d) > 1:
            print(f"[ERROR] Multiple diseases found in cohort")
            for k, v in disease_count_d.items():
                print(f"\t{k}: n={v}")
            print("Only a single disease allowed to create HPOA files.")
            print("Consider using \"target\" argument in create_hpoa_from_phenopackets")
            sys.exit(1)
        else:
            # all is good, print out the disease and number of individuals
            for k, v in disease_count_d.items():
                print(f"\t{k}: n={v}")

    @staticmethod
    def filter_diseases(disease_id, ppkt_list):
        target_list = list()
        for ppkt in ppkt_list:
            for d in ppkt.diseases:
                if d.term.id == disease_id:
                    target_list.append(ppkt)
                    break
        print(f"[INFO] Extracted {(len(target_list))} from {(len(ppkt_list))} phenopackets with {disease_id}\n")
        return target_list


    def create_hpoa_from_phenopackets(self,
                                    pmid:str,
                                    moi:str, ppkt_dir:str="phenopackets",
                                    target:str=None) -> pd.DataFrame:
        """Create an HPO annotation (HPOA) file from the current cohort

        :param pmid: PubMed id for the mode of inheritance
        :type pmid: str
        :param moi: Mode of inheritance (Autosomal dominant, Autosomal recessive, etc)
        :type moi: str
        :param ppkt_dir: Directory with phenopackets Defaults to "phenopackets".
        :param target: Disease id (e.g., OMIM:600123) to select only phenopackets with this disease. Defaults to None.
        :type target: str
        :returns: dataframe representing the HPOA file (which is also written to disk)
        :rtype: pd.DataFrame
        """
        from pyphetools.visualization import PhenopacketIngestor
        from pyphetools.visualization import HpoaTableBuilder
        if not os.path.isdir(ppkt_dir):
            raise FileNotFoundError(f"Could not find directory at {ppkt_dir}")
        ingestor = PhenopacketIngestor(indir=ppkt_dir)
        ppkt_d = ingestor.get_phenopacket_dictionary()
        ppkt_list = list(ppkt_d.values())
        if target is not None:
            ppkt_list = TemplateImporter.filter_diseases(target, ppkt_list)
        TemplateImporter.check_disease_entries(ppkt_list)
        builder = HpoaTableBuilder(phenopacket_list=ppkt_list)
        if moi == "Autosomal dominant":
            builder.autosomal_dominant(pmid)
        elif moi == "Autosomal recessive":
            builder.autosomal_recessive(pmid)
        elif moi == "X-linked inheritance":
            builder.x_linked(pmid)
        elif moi == "X-linked recessive inheritance":
            builder.x_linked_recessive(pmid)
        elif moi == "X-linked dominant inheritance":
            builder.x_linked_dominant()
        else:
            raise ValueError(f"Did not recognize mode of inheritance {moi}")
        hpoa_creator = builder.build()
        hpoa_creator.write_data_frame()
        return hpoa_creator.get_dataframe()
