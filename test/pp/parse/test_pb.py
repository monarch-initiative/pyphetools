import os

import pytest

from pyphetools.pp.v202 import *

import io


class TestProtobuf:
    """
    Test that we can write a :class:`Phenopacket` to protobuf representation and get the same content back.
    """

    @pytest.fixture(scope='class')
    def fpath_retinoblastoma_pb(self, fpath_pp: str) -> str:
        return os.path.join(fpath_pp, 'retinoblastoma.pb')

    @pytest.mark.skip('Only run upon changes in the retinoblastoma Phenopacket')
    def test_dump_retinoblastoma_pb(
            self,
            retinoblastoma: Phenopacket,
            fpath_retinoblastoma_pb: str,
    ):
        with open(fpath_retinoblastoma_pb, 'wb') as fh:
            retinoblastoma.dump_pb(fh)

    def test_round_trip_to_protobuf_and_back(
            self,
            retinoblastoma: Phenopacket,
    ):
        buf = io.BytesIO()

        retinoblastoma.dump_pb(buf)
        buf.seek(0)

        actual = Phenopacket.from_pb(buf)
        assert actual == retinoblastoma

    def test_from_pb(
            self,
            retinoblastoma: Phenopacket,
            fpath_retinoblastoma_pb: str,
    ):
        with open(fpath_retinoblastoma_pb, 'rb') as fh:
            actual = Phenopacket.from_pb(fh)

        assert actual == retinoblastoma
