import unittest
from src.pyphetools.creation import AgeOfDeathColumnMapper, Individual, MetaData
import phenopackets as PPKt



class TestVitalStatus(unittest.TestCase):

    def test_vs1(self):
        aod_d = {
            "7 months": "P7M",
            "10 months": "P10M",
        }
        mapper = AgeOfDeathColumnMapper(column_name='test', string_to_iso_d=aod_d)
        vstatus = mapper.map_cell_to_vital_status("not there")
        self.assertIsNone(vstatus)
        vstatus = mapper.map_cell_to_vital_status("7 months")
        self.assertIsNotNone(vstatus)
        self.assertTrue(isinstance(vstatus, PPKt.VitalStatus))
        self.assertEquals(PPKt.VitalStatus.DECEASED, vstatus.status)
        self.assertEquals("P7M", vstatus.time_of_death.age.iso8601duration)

    def test_vs2(self):
        aod_d = {
            "7 months": "P7M",
            "10 months": "P10M",
        }
        mapper = AgeOfDeathColumnMapper(column_name='test', string_to_iso_d=aod_d)
        vstatus = mapper.map_cell_to_vital_status("10 months")
        self.assertIsNotNone(vstatus)
        self.assertTrue(isinstance(vstatus, PPKt.VitalStatus))
        self.assertEquals(PPKt.VitalStatus.DECEASED, vstatus.status)
        self.assertEquals("P10M", vstatus.time_of_death.age.iso8601duration)

    def test_individual_with_vs(self):
        """Test that we can add a VitalStatus to the phenopacket.
        """
        aod_d = {
            "7 months": "P7M",
            "10 months": "P10M",
        }
        mapper = AgeOfDeathColumnMapper(column_name='test', string_to_iso_d=aod_d)
        vstatus = mapper.map_cell_to_vital_status("10 months")
        i = Individual(individual_id="test")
        i.set_vital_status(vstatus=vstatus)
        ## needed for API
        hpo_version = "fake.version"
        metadata = MetaData(created_by="ORCID:0000-0002-0736-9199")
        metadata.default_versions_with_hpo(version=hpo_version)
        ppkt = i.to_ga4gh_phenopacket(metadata)
        aod = ppkt.subject.vital_status.time_of_death.age.iso8601duration
        self.assertEqual("P10M", aod)
        print(i)