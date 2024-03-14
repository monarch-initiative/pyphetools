import pytest

from ._util import CaseConverter


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
