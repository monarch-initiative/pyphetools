import unittest
import os
from pyphetools import AgeColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')



class TestOptionMapper(unittest.TestCase):

    def test_year(self):
        ageMapper = AgeColumnMapper.by_year()
        p3 = ageMapper.map_cell("3")
        self.assertEquals("P3Y", p3)
        p42 = ageMapper.map_cell("42")
        self.assertEquals("P42Y", p42)
        
    def test_iso8601(self):
        ageMapper = AgeColumnMapper.iso8601()
        p3y = ageMapper.map_cell("P3Y")
        self.assertEquals("P3Y", p3y)
        p3m25d = ageMapper.map_cell("P3Y2M5D")
        self.assertEquals("P3Y2M5D", p3m25d)