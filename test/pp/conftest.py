import typing

import pytest

from pyphetools.pp.v202 import *


@pytest.fixture(scope='package')
def retinoblastoma(
        individual: Individual,
        phenotypic_features: typing.Sequence[PhenotypicFeature],
        biosamples: typing.Sequence[Biosample],
        interpretations: typing.Sequence[Interpretation],
        diseases: typing.Sequence[Disease],
        files: typing.Sequence[File],
        meta_data: MetaData,
) -> Phenopacket:
    """
    Phenopacket with the same values that we can find in `test/data/pp/retinoblastoma.json`.
    """
    return Phenopacket(
        id='example.retinoblastoma.phenopacket.id',
        subject=individual,
        phenotypic_features=phenotypic_features,
        biosamples=biosamples,
        interpretations=interpretations,
        diseases=diseases,
        files=files,
        meta_data=meta_data,
    )


@pytest.fixture(scope='package')
def individual() -> Individual:
    """
    `Individual` from the `retinoblastoma` phenopacket.
    """
    return Individual(
        id='proband A',
        alternate_ids=('some', 'other', 'identifiers'),
        time_at_last_encounter=TimeElement(
            age=Age(
                iso8601duration='P6M',
            )
        ),
        vital_status=VitalStatus(
            status=VitalStatus.Status.DECEASED,
            time_of_death=TimeElement(age=Age(iso8601duration='P1Y')),
            cause_of_death=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            survival_time_in_days=180,
        ),
        sex=Sex.FEMALE,
        karyotypic_sex=KaryotypicSex.XX,
        taxonomy=OntologyClass(id='NCBITaxon:9606', label='Homo sapiens')
    )


@pytest.fixture(scope='package')
def phenotypic_features() -> typing.Sequence[PhenotypicFeature]:
    return (
        PhenotypicFeature(
            type=OntologyClass(id='HP:0030084', label='Clinodactyly'),
            modifiers=(OntologyClass(id='HP:0012834', label='Right'),),
            onset=TimeElement(age=Age(iso8601duration='P3M')),
        ),
        PhenotypicFeature(
            type=OntologyClass(id='HP:0000555', label='Leukocoria'),
            modifiers=(OntologyClass(id='HP:0012835', label='Left'),),
            onset=TimeElement(age=Age(iso8601duration='P4M')),
        ),
        PhenotypicFeature(
            type=OntologyClass(id='HP:0000486', label='Strabismus'),
            modifiers=(OntologyClass(id='HP:0012835', label='Left'),),
            onset=TimeElement(age=Age(iso8601duration='P5M15D')),
        ),
        PhenotypicFeature(
            type=OntologyClass(id='HP:0000541', label='Retinal detachment'),
            modifiers=(OntologyClass(id='HP:0012835', label='Left'),),
            onset=TimeElement(age=Age(iso8601duration='P6M')),
        ),
    )


@pytest.fixture(scope='package')
def diseases() -> typing.Sequence[Disease]:
    return (
        Disease(
            term=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            onset=TimeElement(age=Age(iso8601duration='P4M')),
            disease_stage=(OntologyClass(id='LOINC:LA24739-7', label='Group E'),),
            clinical_tnm_finding=(OntologyClass(id='NCIT:C140678', label='Retinoblastoma cM0 TNM Finding v8'),),
            primary_site=OntologyClass(id='UBERON:0004548', label='left eye'),
        ),
    )


@pytest.fixture(scope='package')
def interpretations() -> typing.Sequence[Interpretation]:
    return (
        Interpretation(
            id='interpretation.id',
            progress_status=Interpretation.ProgressStatus.SOLVED,
            diagnosis=Diagnosis(
                disease=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
                genomic_interpretations=(
                    GenomicInterpretation(
                        subject_or_biosample_id='proband A',
                        interpretation_status=GenomicInterpretation.InterpretationStatus.CAUSATIVE,
                        variant_interpretation=VariantInterpretation(
                            acmg_pathogenicity_classification=AcmgPathogenicityClassification.PATHOGENIC,
                            therapeutic_actionability=TherapeuticActionability.ACTIONABLE,
                            variation_descriptor=VariationDescriptor(
                                id='example-cnv',
                                molecule_context=MoleculeContext.genomic,
                                # TODO: variation
                                extensions=(
                                    Extension(name='mosaicism', value='40.0%'),
                                ),
                            )
                        )
                    ),
                    GenomicInterpretation(
                        subject_or_biosample_id='biosample.1',
                        interpretation_status=GenomicInterpretation.InterpretationStatus.CAUSATIVE,
                        variant_interpretation=VariantInterpretation(
                            acmg_pathogenicity_classification=AcmgPathogenicityClassification.PATHOGENIC,
                            therapeutic_actionability=TherapeuticActionability.ACTIONABLE,
                            variation_descriptor=VariationDescriptor(
                                id='rs121913300',
                                molecule_context=MoleculeContext.genomic,
                                # TODO: variation
                                label='RB1 c.958C>T (p.Arg320Ter)',
                                gene_context=GeneDescriptor(value_id='HGNC:9884', symbol='RB1'),
                                expressions=(
                                    Expression(syntax='hgvs.c', value='NM_000321.2:c.958C>T'),
                                    Expression(syntax='transcript_reference', value='NM_000321.2'),
                                ),
                                vcf_record=VcfRecord(
                                    genome_assembly="GRCh38",
                                    chrom="NC_000013.11",
                                    pos=48367512,
                                    ref="C",
                                    alt="T",
                                ),
                                extensions=(
                                    Extension(name='allele-frequency', value='25.0%'),
                                ),
                                allelic_state=OntologyClass(id='GENO:0000135', label='heterozygous'),
                            )
                        )
                    )
                ),
            ),
        ),
    )


@pytest.fixture(scope='package')
def biosamples() -> typing.Sequence[Biosample]:
    return (
        Biosample(
            id='biosample.1',
            sampled_tissue=OntologyClass(id='UBERON:0000970', label='eye'),
            phenotypic_features=(
                PhenotypicFeature(type=OntologyClass(id='NCIT:C35941', label='Flexner-Wintersteiner Rosette Formation')),
                PhenotypicFeature(type=OntologyClass(id='NCIT:C132485', label='Apoptosis and Necrosis')),
            ),
            # measurements=(), # TODO: add after implementing Measurement
            tumor_progression=OntologyClass(id='NCIT:C8509', label='Primary Neoplasm'),
            pathological_tnm_finding=(
                OntologyClass(id='NCIT:C140720', label='Retinoblastoma pT3 TNM Finding v8'),
                OntologyClass(id='NCIT:C140711', label='Retinoblastoma pN0 TNM Finding v8'),
            ),
            # procedure=,  # TODO: add after implementing Procedure
            files=(
                File(
                    uri='file://data/fileSomaticWgs.vcf.gz',
                    individual_to_file_identifiers={
                        'biosample.1': 'specimen.1',
                    },
                    file_attributes={
                        'fileFormat': 'VCF',
                        'genomeAssembly': 'GRCh38',
                    },
                ),
            ),
        ),
    )


@pytest.fixture(scope='package')
def files() -> typing.Sequence[File]:
    return (
        File(
            uri='file://data/germlineWgs.vcf.gz',
            individual_to_file_identifiers={
                'proband A': 'sample1',
                'proband B': 'sample2'
            },
            file_attributes={
                'fileFormat': 'VCF',
                'genomeAssembly': 'GRCh38',
            },
        ),
        File(
            uri='file://data/somaticWgs.vcf.gz',
            individual_to_file_identifiers={
                'proband A': 'sample1',
                'proband B': 'sample2'
            },
            file_attributes={
                'fileFormat': 'VCF',
                'genomeAssembly': 'GRCh38',
            },
        ),
    )


@pytest.fixture(scope='package')
def meta_data() -> MetaData:
    """
    `MetaData` from the `retinoblastoma` phenopacket.
    """
    return MetaData(
        created=Timestamp.from_str('2021-05-14T10:35:00Z'),
        created_by='anonymous biocurator',
        submitted_by=None,
        resources=(
            Resource(
                id='hp', name='human phenotype ontology',
                url='http://purl.obolibrary.org/obo/hp.owl',
                version='2021-08-02', namespace_prefix='HP',
                iri_prefix='http://purl.obolibrary.org/obo/HP_'
            ),
            Resource(
                id='geno', name='Genotype Ontology',
                url='http://purl.obolibrary.org/obo/geno.owl',
                version='2020-03-08', namespace_prefix='GENO',
                iri_prefix='http://purl.obolibrary.org/obo/GENO_'
            ),
            Resource(
                id='ncit', name='NCI Thesaurus',
                url='http://purl.obolibrary.org/obo/ncit.owl',
                version='VERSION', namespace_prefix='NCIT',
                iri_prefix='http://purl.obolibrary.org/obo/NCIT_'
            ),
            Resource(
                id='uberon', name='Uber-anatomy ontology',
                url='http://purl.obolibrary.org/obo/uberon.owl',
                version='VERSION', namespace_prefix='UBERON',
                iri_prefix='http://purl.obolibrary.org/obo/UBERON_'
            ),
            Resource(
                id='loinc', name='Logical Observation Identifiers Names and Codes',
                url='https://loinc.org',
                version='VERSION', namespace_prefix='LOINC',
                iri_prefix='https://loinc.org'
            ),
            Resource(
                id='drugcentral', name='Drug Central',
                url='https://drugcentral.org/',
                version='VERSION', namespace_prefix='DrugCentral',
                iri_prefix='https://drugcentral.org/drugcard'
            ),
            Resource(
                id='ucum', name='Unified Code for Units of Measure',
                url='https://ucum.org',
                version='2.1', namespace_prefix='UCUM',
                iri_prefix='https://ucum.org/'
            ),
        ),
        phenopacket_schema_version='2.0.0',
    )