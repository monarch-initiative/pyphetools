from pyphetools.pp.v202 import Individual, Phenopacket


class TestMessageMixin:

    def test_from_dict(self, individual: Individual):
        payload = {
            'id': 'example',
            'alternate_ids': ('other', 'yet', 'something'),
            'time_at_last_encounter': {
                'age': {'iso8601duration': 'P11Y6M'}
            }
        }

        individual = Individual.from_dict(payload)

        assert individual.id == 'example'
        assert individual.alternate_ids == ('other', 'yet', 'something')
        assert individual.time_at_last_encounter.age.iso8601duration == 'P11Y6M'

    def test_round_trip(self, retinoblastoma: Phenopacket):
        out = {}
        retinoblastoma.to_dict(out)

        other = Phenopacket.from_dict(out)

        assert retinoblastoma == other
