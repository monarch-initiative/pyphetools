import typing

import pytest

from pyphetools.pp.v202 import *


@pytest.fixture(scope='package')
def retinoblastoma(
        individual: Individual,
        files: typing.Sequence[File],
        meta_data: MetaData,
) -> Phenopacket:
    """
    Phenopacket with the same values that we can find in `test/data/pp/retinoblastoma.json`.
    """
    return Phenopacket(
        id='example.retinoblastoma.phenopacket.id',
        subject=individual,
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
def files() -> typing.Sequence[File]:
    return (
        File(
            uri='file://data/germlineWgs.vcf.gz',
            individual_to_file_identifiers={
                'proband A': 'sample1',
                'proband B': 'sample2'
            },
            file_attributes={
                'genomeAssembly': 'GRCh38',
                'fileFormat': 'VCF',
            },
        ),
        File(
            uri='file://data/somaticWgs.vcf.gz',
            individual_to_file_identifiers={
                'proband A': 'sample1',
                'proband B': 'sample2'
            },
            file_attributes={
                'genomeAssembly': 'GRCh38',
                'fileFormat': 'VCF',
            },
        ),
    )


@pytest.fixture(scope='package')
def meta_data() -> MetaData:
    """
    `MetaData` from the `retinoblastoma` phenopacket.
    """
    return MetaData(
    )
