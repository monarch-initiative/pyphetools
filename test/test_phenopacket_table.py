import unittest
import os
from src.pyphetools.visualization import PhenopacketTable

HP_JSON_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'hp.json')


class TestPhenopacketTable(unittest.TestCase):

    def test_age_1(self):
        iso8601 = "P7Y"
        expected_days = int(365.25 * 7)
        days = PhenopacketTable.iso_to_days(iso_age=iso8601)
        self.assertEqual(expected_days, days)

    def test_age_2(self):
        iso8601 = "P7Y2M"
        expected_days = int(365.25 * 7) + int(30.437*2)
        days = PhenopacketTable.iso_to_days(iso_age=iso8601)
        self.assertEqual(expected_days, days)

    def test_age_3(self):
        iso8601 = "P7Y2M6D"
        expected_days = int(365.25 * 7) + int(30.437*2) + 6
        days = PhenopacketTable.iso_to_days(iso_age=iso8601)
        self.assertEqual(expected_days, days)
