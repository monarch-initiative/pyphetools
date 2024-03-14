import pytest

from pyphetools.pp import JsonSerializer
from pyphetools.pp.v202 import *


class TestJsonSerializer:

    @pytest.fixture
    def serializer(self) -> JsonSerializer:
        return JsonSerializer()

    def test_serialize(self,
                       serializer: JsonSerializer,
                       phenopacket: Phenopacket,
                       ):
        phenopacket.serialize(serializer)
