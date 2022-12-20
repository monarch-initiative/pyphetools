import unittest
import os
from pyphetools import AgeColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')
# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"

class TestOptionMapper(unittest.TestCase):

    def test_year(self):
        ageMapper = AgeColumnMapper.by_year(column_name=TEST_COLUMN)
        p3 = ageMapper.map_cell("3")
        self.assertEquals("P3Y", p3)
        p42 = ageMapper.map_cell("42")
        self.assertEquals("P42Y", p42)
        
    def test_iso8601(self):
        ageMapper = AgeColumnMapper.iso8601(column_name=TEST_COLUMN)
        p3y = ageMapper.map_cell("P3Y")
        self.assertEquals("P3Y", p3y)
        p3m25d = ageMapper.map_cell("P3Y2M5D")
        self.assertEquals("P3Y2M5D", p3m25d)
        
    def test_year_month_both_1(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "14 y 8 m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEquals("P14Y8M", age_iso)
        
    def test_year_month_both_2(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "7 y 6 m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEquals("P7Y6M", age_iso)
        
    def test_year_month_both_3(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "7y6m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEquals("P7Y6M", age_iso)
        
    def test_year_month_just_year_1(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "7 y"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEquals("P7Y", age_iso)
        
    def test_year_month_just_month_1(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "2 m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEquals("P2M", age_iso)