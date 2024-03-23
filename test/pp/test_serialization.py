
from google.protobuf.message import Message

from pyphetools.pp.v202 import *


class TestSerializable:

    def test_to_message__no_compound_fields(self):
        # Test a message with no compound fields.
        oc = OntologyClass(id='HP:0001250', label='Seizure')
        msg = oc.to_message()

        assert isinstance(msg, Message)
        assert msg.id == 'HP:0001250'
        assert msg.label == 'Seizure'

    def test_to_message__with_a_compound_field(self):
        # Test a message with a compound field.
        age_range = AgeRange(start=Age(iso8601duration='P1Y'), end=Age(iso8601duration='P2Y'))
        msg = age_range.to_message()

        assert isinstance(msg, Message)
        assert isinstance(msg.start, Message)
        assert msg.start.iso8601duration == 'P1Y'

        assert isinstance(msg.end, Message)
        assert msg.end.iso8601duration == 'P2Y'

    def test_to_message__map_field(self):
        # Test a message that has a map field.
        file = File(uri='file://path/to/some/file.bam',)
        file.individual_to_file_identifiers['Jim'] = 'jimmy'
        file.individual_to_file_identifiers['Fred'] = 'freddy'

        file.file_attributes['genomeAssembly'] = 'GRCh38'
        file.file_attributes['fileFormat'] = 'BAM'

        msg = file.to_message()

        assert isinstance(msg, Message)
        assert msg.uri == 'file://path/to/some/file.bam'

        assert msg.individual_to_file_identifiers['Jim'] == 'jimmy'
        assert msg.individual_to_file_identifiers['Fred'] == 'freddy'

        assert msg.file_attributes['genomeAssembly'] == 'GRCh38'
        assert msg.file_attributes['fileFormat'] == 'BAM'

    def test_to_message__oneof_field(self):
        te = TimeElement(element=Age(iso8601duration='P1Y'))

        msg = te.to_message()

        assert isinstance(msg, Message)
        assert msg.age.iso8601duration == 'P1Y'

        # Try other one-of case
        te = TimeElement(element=GestationalAge(weeks=6, days=4))

        msg = te.to_message()
        assert isinstance(msg, Message)
        assert msg.gestational_age.weeks == 6
        assert msg.gestational_age.days == 4
