import os

import hpotk
import pytest


@pytest.fixture(scope='session')
def fpath_data() -> str:
    parent = os.path.dirname(__file__)
    return os.path.join(parent, 'data')


@pytest.fixture(scope='session')
def fpath_hpo(fpath_data: str) -> str:
    return os.path.join(fpath_data, 'hp.json')


@pytest.fixture(scope='session')
def hpo(fpath_hpo: str) -> hpotk.Ontology:
    return hpotk.load_ontology(fpath_hpo)
