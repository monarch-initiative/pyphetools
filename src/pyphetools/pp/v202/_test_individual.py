import pytest

from ._individual import Sex


@pytest.mark.parametrize(
    'left, right, expected',
    [
        (Sex.MALE, Sex.MALE, True),
        (Sex.FEMALE, Sex.FEMALE, True),
        (Sex.OTHER_SEX, Sex.OTHER_SEX, True),
        (Sex.UNKNOWN_SEX, Sex.UNKNOWN_SEX, True),

        (Sex.FEMALE, Sex.MALE, False),
        (Sex.MALE, Sex.FEMALE, False),
    ]
)
def test_sex_eq(left: Sex, right: Sex, expected: bool):
    assert (left == right) == expected
