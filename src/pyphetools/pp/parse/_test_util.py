import pytest

from ._util import CaseConverter
from ._util import HierarchicalKeyMapper


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

            # The snake case is, however, left untouched.
            ('abc_def', 'abc_def'),
            ('abc_def_g_h', 'abc_def_g_h'),
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


class TestHierarchicalKeyMapper:

    @pytest.fixture
    def mapper(self) -> HierarchicalKeyMapper:
        return HierarchicalKeyMapper((
            'file_attributes', 'individual_to_file_identifiers',
            'fileAttributes', 'individualToFileIdentifiers',
        ))

    @pytest.fixture
    def case_converter(self) -> CaseConverter:
        return CaseConverter()

    def test_remap(
            self,
            mapper: HierarchicalKeyMapper,
            case_converter: CaseConverter,
    ):
        payload = {
          "files": [
            {
              "uri": "file://data/germlineWgs.vcf.gz",
              "individual_to_file_identifiers": {"proband A": "sample1", "proband B": "sample2", },
              "file_attributes": {"genome_assembly": "GRCh38", "file_format": "VCF", }
            }, {
              "uri": "file://data/somaticWgs.vcf.gz",
              "individual_to_file_identifiers": {"proband A": "sample1", "proband B": "sample2", },
              "file_attributes": { "genome_assembly": "GRCh38", "file_format": "VCF", }
            }
          ]
        }

        remapped = mapper.remap_mapping(case_converter.snake_to_camel, payload)

        # We remapped the fields
        assert all('individualToFileIdentifiers' in f for f in remapped['files'])
        assert all('fileAttributes' in f for f in remapped['files'])

        # but not their sub-elements.
        for file in remapped['files']:
            assert all(x in file['individualToFileIdentifiers'] for x in ('proband A', 'proband B'))
            assert all(x in file['fileAttributes'] for x in ('genome_assembly', 'file_format'))
