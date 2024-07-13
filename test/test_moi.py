import pytest

from pyphetools.creation import Moi


class TestMoi:

    @pytest.mark.parametrize(
        'moi, hpterm_id, hpterm_label',
        [
            (
                    Moi.AD,
                    'HP:0000006', 
                    'Autosomal dominant inheritance',
            ),
            (
                    Moi.AR,
                    'HP:0000007',
                    'Autosomal recessive inheritance',
            ),
            (
                Moi.XLI,
                'HP:0001417',
                'X-linked inheritance'
            ),
            (
                Moi.XLR,
                'HP:0001419',
                'X-linked recessive inheritance'
            ),
            (
                Moi.XLD,
                'HP:0001423',
                'X-linked dominant inheritance'
            ),
            (
                Moi.MITO,
                'HP:0001427',
                'Mitochondrial inheritance'
            ),
            (
                Moi.YLI,
                'HP:0001450',
                'Y-linked inheritance'
            )

        ]
    )
    def test_moi(
        self,
        moi: Moi, 
        hpterm_id: str, 
        hpterm_label: str,
    ):
        hpterm = moi.to_HPO()

        assert hpterm_id == hpterm.id
        assert hpterm_label == hpterm.label

