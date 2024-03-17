from argparse import ArgumentParser
import os, sys
import pandas as pd
from collections import defaultdict
import typing
from IPython.display import display, HTML
pd.set_option('display.max_colwidth', None) # show entire column contents, important!


def _get_data_from_template(df:pd.DataFrame):
    """Check that the template (dataframe) has the columns
    "HGNC_id", "gene_symbol", "transcript",
    If each row has the same value for these columns, then the template is valid
    and we can proceed.

    :param df: the template with data about a cohort
    :type df: pd.DataFrame
    """

    contents_d = defaultdict(set)
    for item in ["disease_id", "disease_label", "HGNC_id", "gene_symbol", "transcript"]:
        if item not in df.columns:
            raise ValueError(f"Invalid template -- could not find the \"{item}\" column")
    ## We need to skip the first row, which has the datatypes
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
    # we know there is only one element, which we get with "pop"
    disease_id = contents_d.get("disease_id").pop()
    disease_label = contents_d.get("disease_label").pop()
    HGNC_id = contents_d.get("HGNC_id").pop()
    gene_symbol = contents_d.get("gene_symbol").pop()
    transcript = contents_d.get("transcript").pop()
    return disease_id, disease_label, HGNC_id, gene_symbol, transcript


def import_phenopackets_from_template(template:str, hp_json:str,
                                      deletions:typing.Set[str]=set(),
                                      duplications:typing.Set[str]=set(),
                                      inversions:typing.Set[str]=set(),):
    from pyphetools.creation  import HpoParser
    from pyphetools.creation import CaseTemplateEncoder, AllelicRequirement
    from pyphetools.creation import VariantManager
    from pyphetools.validation import CohortValidator
    if not os.path.isfile(template):
        raise FileNotFoundError(f"Could not find template file {template}")
    if not os.path.isfile(hp_json):
        raise FileNotFoundError(f"Could not find hp.json file at {hp_json}")
    parser = HpoParser(hpo_json_file=hp_json)
    hpo_cr = parser.get_hpo_concept_recognizer()
    hpo_ontology = parser.get_ontology()
    created_by="ORCID:0000-0002-0736-9199"
    print(f"HPO version {hpo_ontology.version}")
    df = pd.read_excel(template)
    encoder = CaseTemplateEncoder(df=df, hpo_cr=hpo_cr, created_by=created_by, hpo_ontology=hpo_ontology)
    individuals = encoder.get_individuals()
    disease_id, disease_label, HGNC_id, gene_symbol, transcript = _get_data_from_template(df)
    print(f" we got {disease_id}  {transcript}")
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
    vman.add_variants_to_individuals(individuals)
    cvalidator = CohortValidator(cohort=individuals, ontology=hpo_ontology, min_hpo=1, allelic_requirement=AllelicRequirement.MONO_ALLELIC)
    ef_individuals = cvalidator.get_error_free_individual_list()
    encoder.output_individuals_as_phenopackets(individual_list=ef_individuals)
    return individuals, cvalidator






def create_hpoa_from_phenopackets(pmid:str, moi:str, ppkt_dir:str="phenopackets") -> pd.DataFrame:
    from pyphetools.visualization import PhenopacketIngestor
    from pyphetools.visualization import HpoaTableBuilder
    if not os.path.isdir(ppkt_dir):
        raise FileNotFoundError(f"Could not find directory at {ppkt_dir}")
    ingestor = PhenopacketIngestor(indir=ppkt_dir)
    ppkt_d = ingestor.get_phenopacket_dictionary()
    ppkt_list = list(ppkt_d.values())
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
