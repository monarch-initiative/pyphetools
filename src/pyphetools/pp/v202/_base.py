import typing

from .._api import MessageMixin


class GestationalAge(MessageMixin):

    def __init__(
            self,
            weeks: int,
            days: typing.Optional[int],
    ):
        # TODO: validate
        self._weeks = weeks
        self._days = days

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'weeks', 'days',

    @property
    def weeks(self) -> int:
        return self._weeks

    @weeks.setter
    def weeks(self, value: int):
        self._weeks = value

    @property
    def days(self) -> typing.Optional[int]:
        return self._days

    @days.setter
    def days(self, value: typing.Optional[int]):
        self._weeks = value

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'weeks' in values:
            weeks = values['weeks']
            days = values['days'] if 'days' in values else None
            return GestationalAge(
                weeks=weeks,
                days=days,
            )
        else:
            raise ValueError('Bug')  # TODO: better message

    def __eq__(self, other):
        return isinstance(other, GestationalAge) \
            and self._weeks == other._weeks \
            and self._days == other._days

    def __repr__(self):
        return f'GestationalAge(weeks={self._weeks}, days={self._days})'


class Age(MessageMixin):

    def __init__(
            self,
            iso8601duration: str,
    ):
        self._iso8601duration = iso8601duration

    @property
    def iso8601duration(self) -> str:
        return self._iso8601duration

    @iso8601duration.setter
    def iso8601duration(self, value: str):
        self._iso8601duration = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'iso8601duration',

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'iso8601duration' in values:
            return Age(iso8601duration=values['iso8601duration'])
        else:
            raise ValueError('Cannot deserialize')  # TODO: wording

    def __eq__(self, other):
        return isinstance(other, Age) \
            and self._iso8601duration == other._iso8601duration

    def __repr__(self):
        return f'Age(iso8601duration={self._iso8601duration})'


class AgeRange(MessageMixin):

    def __init__(
            self,
            start: Age,
            end: Age,
    ):
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: Age):
        self._start = value

    @property
    def end(self) -> Age:
        return self._end

    @end.setter
    def end(self, value: Age):
        self._end = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'start', 'end'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'start' in values and 'end' in values:
            return AgeRange(
                start=Age.from_dict(values['start']),
                end=Age.from_dict(values['end']),
            )
        else:
            raise ValueError('Cannot deserialize')  # TODO: wording

    def __eq__(self, other):
        return isinstance(other, AgeRange) \
            and self._start == other._start \
            and self._end == other._end

    def __repr__(self):
        return f'AgeRange(start={self._start}, end={self._end})'


class TimeElement(MessageMixin):

    def __init__(
            self,
            gestational_age: typing.Optional[GestationalAge] = None,
            age: typing.Optional[Age] = None,
            age_range: typing.Optional[AgeRange] = None,
            # TODO:
            #  OntologyClass ontology_class = 3;
            #  google.protobuf.Timestamp timestamp = 4;
            #  TimeInterval interval = 5;
    ):
        # exactly one one-of field must be set!
        one_ofs = (gestational_age, age, age_range)
        if sum(1 for arg in one_ofs if arg is not None) != 1:
            self._complain_about_inputs(one_ofs)
        if gestational_age is not None:
            self._discriminant = 6
            self._val = gestational_age
        elif age is not None:
            self._discriminant = 1
            self._val = age
        elif age_range is not None:
            self._discriminant = 2
            self._val = age_range
        else:
            raise ValueError('Bug')  # TODO: wording

    @property
    def age(self) -> typing.Optional[Age]:
        return self._val if self._discriminant == 1 else None

    @age.setter
    def age(self, value: Age):
        self._discriminant = 1
        self._val = value

    @property
    def age_range(self) -> typing.Optional[AgeRange]:
        return self._val if self._discriminant == 2 else None

    @age_range.setter
    def age_range(self, value: AgeRange):
        self._discriminant = 2
        self._val = value

    @property
    def gestational_age(self) -> typing.Optional[GestationalAge]:
        return self._val if self._discriminant == 6 else None

    @gestational_age.setter
    def gestational_age(self, value: GestationalAge):
        self._discriminant = 6
        self._val = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'gestational_age', 'age', 'age_range',  # TODO

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        # TODO: should only have one key!
        if 'gestational_age' in values:
            return TimeElement(gestational_age=GestationalAge.from_dict(values['gestational_age']))
        elif 'age' in values:
            return TimeElement(age=Age.from_dict(values['age']))
        elif 'age_range' in values:
            return TimeElement(age_range=AgeRange.from_dict(values['age_range']))
        elif 'ontology_class' in values:
            # TODO:
            pass
        elif 'timestamp' in values:
            # TODO:
            pass
        elif 'interval' in values:
            # TODO:
            pass
        else:
            raise ValueError('Bug')  # TODO: better message

    def _complain_about_inputs(self, args):
        # TODO - different error
        raise ValueError('Some error happened here!')

    def __eq__(self, other):
        return isinstance(other, TimeElement) \
            and self._discriminant == other._discriminant \
            and self._val == other._val

    def __repr__(self):
        if self._discriminant == 1:
            val = f'age={self._val}'
        elif self._discriminant == 2:
            val = f'age_range={self._val}'
        elif self._discriminant == 3:
            val = f'ontology_class={self._val}'
        elif self._discriminant == 4:
            val = f'timestamp={self._val}'
        elif self._discriminant == 5:
            val = f'interval={self._val}'
        elif self._discriminant == 6:
            val = f'gestational_age={self._val}'
        else:
            raise ValueError(f'Invalid discriminant {self._discriminant}')

        return f'TimeElement({val})'
