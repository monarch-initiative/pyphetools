import typing

import pytest

from pyphetools.pp.v202 import *


@pytest.fixture(scope='package')
def retinoblastoma(
        individual: Individual,
        phenotypic_features: typing.Sequence[PhenotypicFeature],
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
