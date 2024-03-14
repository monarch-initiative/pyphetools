import pytest

from pyphetools.pp.v202 import *


@pytest.fixture(scope='package')
def individual() -> Individual:
    return Individual(
        id='example',
        alternate_ids=('other', 'yet', 'something'),
        time_at_last_encounter=TimeElement(
            age=Age(
                iso8601duration='P11Y6M'
            )
        )
    )


@pytest.fixture(scope='package')
def meta_data() -> MetaData:
    return MetaData(
    )


@pytest.fixture(scope='package')
def phenopacket(
        individual: Individual,
        meta_data: MetaData,
) -> Phenopacket:
    return Phenopacket(
        id='pp-id',
        subject=individual,
        meta_data=meta_data,
    )
