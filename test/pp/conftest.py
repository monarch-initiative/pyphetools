import pytest

from pyphetools.pp.v202 import *


@pytest.fixture(scope='package')
def retinoblastoma(
        individual: Individual,
        meta_data: MetaData,
) -> Phenopacket:
    """
    Phenopacket with the same values that we can find in `test/data/pp/retinoblastoma.json`.
    """
    return Phenopacket(
        id='arbitrary.id',
        subject=individual,
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
        )
    )


@pytest.fixture(scope='package')
def meta_data() -> MetaData:
    """
    `MetaData` from the `retinoblastoma` phenopacket.
    """
    return MetaData(
    )
