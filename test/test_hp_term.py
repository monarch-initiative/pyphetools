import unittest

from pyphetools.creation import HpTerm, HpTermBuilder, IsoAge


class TestHpTerm(unittest.TestCase):

    def test_excluded(self):
        hpo_term = HpTerm(hpo_id="HP:0001250", label="test label")
        self.assertEqual("HP:0001250", hpo_term.id)
        self.assertEqual("test label", hpo_term.label)
        self.assertTrue(hpo_term.observed)
        self.assertTrue(hpo_term.measured)
        hpo_term.excluded()
        self.assertFalse(hpo_term.observed)


    def test_create_phenotypic_feature(self):
        """test creation of GA4GH PhenotypicFeature object with onset and resolution
        """
        hpo_term = HpTerm(hpo_id="HP:0001250", label="test label", onset=IsoAge.from_iso8601("P2M"), resolution=IsoAge.from_iso8601("P6M"))
        self.assertEqual("HP:0001250", hpo_term.id)
        self.assertEqual("test label", hpo_term.label)
        self.assertEqual("P2M", hpo_term.onset.age_string)
        self.assertEqual("P6M", hpo_term.resolution.age_string)
        self.assertTrue(hpo_term.observed)
        self.assertTrue(hpo_term.measured)
        pfeat = hpo_term.to_ga4gh_phenotypic_feature()
        self.assertIsNotNone(pfeat)
        pfterm = pfeat.type
        self.assertEqual("HP:0001250", pfterm.id)
        self.assertEqual("test label", pfterm.label)
        self.assertEqual("P2M", pfeat.onset.age.iso8601duration)
        self.assertEqual("P6M", pfeat.resolution.age.iso8601duration)
        self.assertFalse(pfeat.excluded)


    def test_fetal_onset(self):
        hpterm = HpTermBuilder(hpo_id="HP:0010942", hpo_label="Echogenic intracardiac focus").fetal_onset().build()
        self.assertEqual("HP:0010942", hpterm.id)
        self.assertEqual("Echogenic intracardiac focus", hpterm.label)
        self.assertIsNotNone(hpterm.onset)
        self.assertTrue(hpterm.onset.is_valid())
        onset_term = hpterm.onset
        print(type(onset_term))
        # Fetal onset HP:0011461
        self.assertEqual("Fetal onset", onset_term.age_string)
        #self.assertEqual("HP:0011461", onset_term[1])
        phenotypic_feature = hpterm.to_ga4gh_phenotypic_feature()
        self.assertIsNotNone(phenotypic_feature.onset)
        self.assertIsNotNone(phenotypic_feature.onset.ontology_class)
        oclass = phenotypic_feature.onset.ontology_class
        self.assertEqual("HP:0011461", oclass.id)
        self.assertEqual("Fetal onset", oclass.label)

    def test_late_onset(self):
        hpterm = HpTermBuilder(hpo_id="HP:0000726", hpo_label="Dementia").late_onset().build()
        self.assertEqual("HP:0000726", hpterm.id)
        self.assertEqual("Dementia", hpterm.label)
        self.assertTrue(hpterm.onset.is_valid())
        self.assertIsNotNone(hpterm.onset)
        onset_term = hpterm.onset
        # Late onset HP:0003584
        self.assertEqual("Late onset", onset_term.age_string)
        phenotypic_feature = hpterm.to_ga4gh_phenotypic_feature()
        self.assertIsNotNone(phenotypic_feature.onset)
        self.assertIsNotNone(phenotypic_feature.onset.ontology_class)
        oclass = phenotypic_feature.onset.ontology_class
        self.assertEqual("HP:0003584", oclass.id)
        self.assertEqual("Late onset", oclass.label)




