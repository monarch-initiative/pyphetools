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


@pytest.fixture(scope='session')
def fpath_pp(fpath_data: str) -> str:
    return os.path.join(fpath_data, 'pp')


@pytest.fixture(scope='session')
def fpath_retinoblastoma_json(fpath_pp: str) -> str:
    """
    Path to a JSON file with retinoblastoma phenopacket.

    Note: the phenopacket is pulled from *Phenopacket tools*.
    """
    return os.path.join(fpath_pp, 'retinoblastoma.json')
