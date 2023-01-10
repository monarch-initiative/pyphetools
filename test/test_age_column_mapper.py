import unittest
import os
import re
from pyphetools.creation import AgeColumnMapper

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')
# The API requires us to pass a column name but the column name will not be used in the tests
TEST_COLUMN = "test"

class TestOptionMapper(unittest.TestCase):

    def test_year(self):
        ageMapper = AgeColumnMapper.by_year(column_name=TEST_COLUMN)
        p3 = ageMapper.map_cell("3")
        self.assertEqual("P3Y", p3)
        p42 = ageMapper.map_cell("42")
        self.assertEqual("P42Y", p42)
        
    def test_iso8601(self):
        ageMapper = AgeColumnMapper.iso8601(column_name=TEST_COLUMN)
        p3y = ageMapper.map_cell("P3Y")
        self.assertEqual("P3Y", p3y)
        p3m25d = ageMapper.map_cell("P3Y2M5D")
        self.assertEqual("P3Y2M5D", p3m25d)
        
    def test_year_month_both_1(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "14 y 8 m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P14Y8M", age_iso)
        
    def test_year_month_both_2(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "7 y 6 m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P7Y6M", age_iso)
        
    def test_year_month_both_3(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "7y6m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P7Y6M", age_iso)
        
    def test_year_month_just_year_1(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "7 y"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P7Y", age_iso)
        
    def test_year_month_just_month_1(self):
        ageMapper = AgeColumnMapper.by_year_and_month(column_name=TEST_COLUMN)
        age_string = "2 m"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P2M", age_iso)

    def test_int_or_float_regex(self):
        int_or_float = r"(\d+)(\.\d+)?"
        p=re.compile(int_or_float)
        y_only = "42"
        results = p.search(y_only).groups()
        self.assertEqual(2, len(results))
        self.assertEqual('42', results[0])
        self.assertIsNone(results[1])
        y_and_m = "42.25"
        results = p.search(y_and_m).groups()
        self.assertEqual(2, len(results))
        self.assertEqual('42', results[0])
        self.assertEqual('.25', results[1])

    def test_fractional_year_strings(self):
        ageMapper = AgeColumnMapper.by_year(column_name=TEST_COLUMN)
        age_string = "2"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P2Y", age_iso)
        age_string = "4.75"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P4Y9M", age_iso)
        age_string = "5.9"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P5Y11M", age_iso)
        age_string = "6.25"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P6Y3M", age_iso)
        age_string = "8.1"
        age_iso = ageMapper.map_cell(age_string)
        self.assertEqual("P8Y1M", age_iso)

