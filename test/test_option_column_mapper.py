import unittest
import os
from src.pyphetools.creation import HpoParser, OptionColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestOptionMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        parser = HpoParser(hpo_json_file=HP_JSON_FILENAME)
        cls.hpo_cr = parser.get_hpo_concept_recognizer()
        cls.severity_d = {'mild': 'Intellectual disability, mild',
                        'moderate': 'Intellectual disability, moderate',
                        'severe': 'Intellectual disability, severe'
                        }

    def test_hpo_cr_mild(self):
        """We should retrieve Intellectual disability, mild (HP:0001256)"""
        optionMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=self.severity_d)
        results = optionMapper.map_cell("mild")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0001256", result.id)
        self.assertEqual("Intellectual disability, mild", result.label)

    def test_hpo_cr_moderate(self):
        """We should retrieve Intellectual disability, moderate (HP:0002342)"""
        optionMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=self.severity_d)
        results = optionMapper.map_cell("moderate")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0002342", result.id)
        self.assertEqual("Intellectual disability, moderate", result.label)

    def test_hpo_cr_severe(self):
        """We should retrieve Intellectual disability, severe (HP:0010864) """
        optionMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=self.severity_d)
        results = optionMapper.map_cell("severe")
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("HP:0010864", result.id)
        self.assertEqual("Intellectual disability, severe", result.label)

    def test_with_acronyms(self):
        other_d = {
            "HP": "High palate",
            "D": "Dolichocephaly",
            "En": "Deeply set eye",  # i.e., Enophthalmus
            "DE": "Dural ectasia",
            "St": "Striae distensae"
        }
        otherMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=other_d)
        res1 = otherMapper.map_cell("HP")
        res1.sort(key=lambda x: x.label) # sort alphabetically
        self.assertIsNotNone(res1)
        self.assertEqual(1, len(res1))
        hpterm = res1[0]
        self.assertEqual("High palate", hpterm.label)
        self.assertEqual("HP:0000218", hpterm.id)
        res2 = otherMapper.map_cell("HP,D")
        res2.sort(key=lambda x: x.label) # sort alphabetically
        self.assertIsNotNone(res2)
        self.assertEqual(2, len(res2))
        hpterm = res2[0]
        self.assertEqual("Dolichocephaly", hpterm.label)
        self.assertEqual("HP:0000268", hpterm.id)
        hpterm = res2[1]
        self.assertEqual("High palate", hpterm.label)
        self.assertEqual("HP:0000218", hpterm.id)

    def test_eso(self):
        oph_d = {"strabismus": "Strabismus",
                "esotropia": "Esotropia"}
        ophMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=oph_d)
        res = ophMapper.map_cell("right sided esotropia")
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        hpterm = res[0]
        self.assertEqual("Esotropia", hpterm.label)
        self.assertEqual("HP:0000565", hpterm.id)

    def test_option_list(self):
        thumb_d = {"BT": "Broad thumb",
                    "BH": "Broad hallux",
                    "+": ["Broad thumb", "Broad hallux"]}
        thumbMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=thumb_d)
        res = thumbMapper.map_cell("+")
        res.sort(key=lambda x: x.label) # sort alphabetically
        self.assertIsNotNone(res)
        self.assertEqual(2, len(res))
        hpterm0 = res[0]
        self.assertEqual("Broad hallux", hpterm0.label)
        self.assertEqual("HP:0010055", hpterm0.id)
        hpterm1 = res[1]
        self.assertEqual("Broad thumb", hpterm1.label)
        self.assertEqual("HP:0011304", hpterm1.id)

    def test_options_broad(self):
        thumb_d = {"BT": "Broad thumb",
                    "BH": "Broad hallux",
                    "+": [ "Broad thumb", "Broad hallux"]}
        thumbMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=thumb_d)
        res = thumbMapper.map_cell("BT, BH")
        res.sort(key=lambda x: x.label) # sort alphabetically
        self.assertIsNotNone(res)
        self.assertEqual(2, len(res))
        hpterm0 = res[0]
        self.assertEqual("Broad hallux", hpterm0.label)
        self.assertEqual("HP:0010055", hpterm0.id)
        hpterm1 = res[1]
        self.assertEqual("Broad thumb", hpterm1.label)
        self.assertEqual("HP:0011304", hpterm1.id)

    def test_options_negative(self):
        thumb_d = {"BT": "Broad thumb",
                "BH": "Broad hallux",
                "+": ["Broad thumb", "Broad hallux"]}
        excluded_d = {"-":"Broad thumb"}
        thumbMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr, option_d=thumb_d,
                                        excluded_d=excluded_d)
        res = thumbMapper.map_cell("-")
        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        hpterm0 = res[0]
        self.assertEqual("Broad thumb", hpterm0.label)
        self.assertEqual("HP:0011304", hpterm0.id)
        self.assertFalse(hpterm0.observed)


    def test_avoid_duplicates(self):
        """
        avoid adding the same term multiple times if one item is a substring of another
        """
        autistic_like_behavior_d = {
            'stereotypies': 'Motor stereotypy',
            'yes - was being investigated': 'Autism',
            'Severe autism': 'Autism',
            'yes': 'Autism'}
        exluded_d = {'no': 'Autism',
                    'no formal testing (no concern for ASD)': 'Autism', }
        autisticMapper = OptionColumnMapper(concept_recognizer=self.hpo_cr,
                                            option_d=autistic_like_behavior_d,
                                            excluded_d=exluded_d)
        hpo_term_list = autisticMapper.map_cell("yes - was being investigated")
        self.assertEqual(1, len(hpo_term_list))

    def test_metabolic(self):
        """
        This test is for cases where the slash could be misinterpreted as a delimiter
        Now the code checks first for exact matches with the cell contents and the options_d
        """
        urine_xa_d = {'11.7umol/mmolCr': "Xanthinuria",
                    '1.7umol/mmolCr': "Xanthinuria"}
        urine_not_xa_d = {'0.04mmol/L': "Xanthinuria",
                        "1.6umol/mmolCr": "Xanthinuria",
                        "0.0214XA/Cr": "Xanthinuria",
                        "normal": "Xanthinuria"}
        urineXAmapper = OptionColumnMapper(concept_recognizer=self.hpo_cr,
                                        option_d=urine_xa_d,
                                        excluded_d=urine_not_xa_d)
        hpo_term_list = urineXAmapper.map_cell('11.7umol/mmolCr')
        self.assertEqual(1, len(hpo_term_list))
        hpterm = hpo_term_list[0]
        self.assertEqual("Xanthinuria", hpterm.label)
        self.assertEqual("HP:0010934", hpterm.id)



