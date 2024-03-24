import io

import pytest

from pyphetools.pp.parse.json import JsonSerializer, JsonDeserializer
from pyphetools.pp.v202 import *


class TestJsonSerializers:

    @pytest.fixture
    def serializer(self) -> JsonSerializer:
        return JsonSerializer(indent=2)

    @pytest.fixture
    def deserializer(self) -> JsonDeserializer:
        return JsonDeserializer()

    def test_deserialize(
            self,
            fpath_retinoblastoma_json: str,
            retinoblastoma: Phenopacket,
            deserializer: JsonDeserializer,
    ):
        with open(fpath_retinoblastoma_json) as fh:
            pp = deserializer.deserialize(fh, Phenopacket)

        assert pp == retinoblastoma

    def test_round_trip(
            self,
            retinoblastoma: Phenopacket,
            serializer: JsonSerializer,
            deserializer: JsonDeserializer,
    ):
        # Serialize
        buf = io.StringIO()
        serializer.serialize(retinoblastoma, buf)

        # Deserialize
        buf.seek(0)  # Rewind to allow reading from the buffer.
        out = deserializer.deserialize(buf, Phenopacket)

        # Compare
        assert out == retinoblastoma
