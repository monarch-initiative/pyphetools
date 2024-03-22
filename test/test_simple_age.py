import unittest
from pyphetools.visualization import SimpleAge


class TestSimpleAge(unittest.TestCase):

    def test_1month_1week(self):
        sa = SimpleAge(age_string="P1M1W")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003593", onset_term.id)
        self.assertEqual("Infantile onset", onset_term.label)

    def test_1week(self):
        sa = SimpleAge(age_string="P1W")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003623", onset_term.id)
        self.assertEqual("Neonatal onset", onset_term.label)

    def test_1day(self):
        sa = SimpleAge(age_string="P1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003577", onset_term.id)
        self.assertEqual("Congenital onset", onset_term.label)

    def test_0day(self):
        sa = SimpleAge(age_string="P0D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003577", onset_term.id)
        self.assertEqual("Congenital onset", onset_term.label)

    def test_2Y3M1D(self):
        sa = SimpleAge(age_string="P2Y3M1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0011463", onset_term.id)
        self.assertEqual("Childhood onset", onset_term.label)

    def test_11y(self):
        sa = SimpleAge(age_string="P11Y1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003621", onset_term.id)
        self.assertEqual("Juvenile onset", onset_term.label)

    def test_18y(self):
        sa = SimpleAge(age_string="P18Y2M1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0011462", onset_term.id)
        self.assertEqual("Early young adult onset", onset_term.label)

    def test_22y(self):
        sa = SimpleAge(age_string="P22Y7M1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0025709", onset_term.id)
        self.assertEqual("Intermediate young adult onset", onset_term.label)


    def test_39y(self):
        sa = SimpleAge(age_string="P39Y7M1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0025710", onset_term.id)
        self.assertEqual("Late young adult onset", onset_term.label)

    def test_mideval(self):
        sa = SimpleAge(age_string="P45Y7M1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003596", onset_term.id)
        self.assertEqual("Middle age onset", onset_term.label)

    def test_late(self):
        sa = SimpleAge(age_string="P95Y7M1D")
        onset_term = sa.to_hpo_onset_term()
        self.assertEqual("HP:0003584", onset_term.id)
        self.assertEqual("Late onset", onset_term.label)



