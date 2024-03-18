import pytest

from ._util import CaseConverter
# from ._util import HierarchicalKeyMapper


class TestCaseConverter:

    @pytest.fixture(scope='class')
    def converter(self) -> CaseConverter:
        return CaseConverter()

    @pytest.mark.parametrize(
        'payload, expected',
        [
            ('', ''),
            ('a', 'a'),
            ('A', 'a'),
            ('AbcDef', 'abc_def'),
            ('abcDef', 'abc_def'),
            ('ABcDef', 'a_bc_def'),
            ('ABCDEF', 'a_b_c_d_e_f'),
        ]
    )
    def test_camel_to_snake(
            self,
            converter: CaseConverter,
            payload: str,
            expected: str,
    ):
        actual = converter.camel_to_snake(payload)

        assert actual == expected

    @pytest.mark.parametrize(
        'payload, expected',
        [
            ('', ''),
            ('a', 'a'),
            ('a_', 'a'),
            ('a_b_', 'aB'),
            ('abc', 'abc'),
            ('a_b_c', 'aBC'),
            ('abc_def', 'abcDef'),
            ('a_bc_def', 'aBcDef'),
            ('a_b_c_d_e_f', 'aBCDEF'),
        ]
    )
    def test_snake_to_camel(
            self,
            converter: CaseConverter,
            payload: str,
            expected: str,
    ):
        actual = converter.snake_to_camel(payload)

        assert actual == expected


# class TestHierarchicalKeyMapper:
#
#     @pytest.fixture
#     def payload(self) -> typing.Mapping[str, typing.Any]:
#         payload = """
#         {
#           "files": [
#             {
#               "uri": "file://data/germlineWgs.vcf.gz",
#               "individual_to_file_identifiers": {
#                 "proband A": "sample1",
#                 "proband B": "sample2"
#               },
#               "file_attributes": {
#                 "genome_assembly": "GRCh38",
#                 "file_format": "VCF"
#               }
#             }, {
#               "uri": "file://data/somaticWgs.vcf.gz",
#               "individual_to_file_identifiers": {
#                 "proband A": "sample1",
#                 "proband B": "sample2"
#               },
#               "file_attributes": {
#                 "genome_assembly": "GRCh38",
#                 "file_format": "VCF"
#               }
#             }
#           ]
#         }
#         """
#         return json.loads(payload)
#
#
#     @pytest.fixture
#     def case_converter(self) -> CaseConverter:
#         return CaseConverter()
#
#     def test_remap(
#             self,
#             payload: typing.Mapping[str, typing.Any],
#             case_converter: CaseConverter,
#     ):
#         mapper = HierarchicalKeyMapper(blacklist=('individual_to_file_identifiers',))
#
#         remapped = mapper.remap(case_converter.snake_to_camel, payload)
#         print(remapped)
