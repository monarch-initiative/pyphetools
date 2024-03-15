import typing

from .._api import MessageMixin
from ..parse import extract_message_scalar


class Timestamp(MessageMixin):
    # TODO: implement!
    # '%Y-%m-%dT%H:%M:%S.%fZ'

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return ()

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        return Timestamp()

    def __eq__(self, other):
        return isinstance(other, Timestamp)

    def __repr__(self):
        return f'Timestamp()'


class OntologyClass(MessageMixin):
    """
    `OntologyClass` represents classes (terms) from ontologies, and is used in many places throughout
    the Phenopacket standard. It is a simple, two element message that represents the `identifier` and the `label`
    of an ontology class.

    >>> from pyphetools.pp.v202 import OntologyClass

    >>> oc = OntologyClass(id='HP:0001250', label='Seizure')
    >>> oc.id
    'HP:0001250'
    >>> oc.label
    'Seizure'

    :param id: a `str` with a CURIE-style identifier (e.g. `HP:0001250`).
    :param label: a `str` with a human-readable class name (e.g. `Seizure`).
    """

    def __init__(
            self,
            id: str,
            label: str,
    ):
        self._id = id
        self._label = label

    @property
    def id(self) -> str:
        """
        Get a `str` with the ontology class identifier.
        """
        return self._id

    @property
    def label(self) -> str:
        """
        Get a `str` with the human-readable class name.
        """
        return self._label

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'label'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'id' in values and 'label' in values:
            return OntologyClass(
                id=values['id'],
                label=values['label'],
            )

    def __eq__(self, other):
        return isinstance(other, OntologyClass) \
            and self._id == other._id \
            and self._label == other._label

    def __repr__(self):
        return f'OntologyClass(id={self._id}, label={self._label})'


class ExternalReference(MessageMixin):

    def __init__(
            self,
            id: typing.Optional[str] = None,
            reference: typing.Optional[str] = None,
            description: typing.Optional[str] = None,
    ):
        self._id = id
        self._reference = reference
        self._description = description

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def reference(self) -> str:
        return self._reference

    @reference.setter
    def reference(self, value: str):
        self._reference = value

    @reference.deleter
    def reference(self):
        self._reference = None

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @description.deleter
    def description(self):
        self._description = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'reference', 'description'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        return ExternalReference(
            id=MessageMixin._extract_optional_field('id', values),
            reference=MessageMixin._extract_optional_field('reference', values),
            description=MessageMixin._extract_optional_field('description', values),
        )

    def __eq__(self, other):
        return isinstance(other, ExternalReference) \
            and self._id == other._id \
            and self._reference == other._reference \
            and self._description == other._description

    def __repr__(self):
        return f'ExternalReference(id={self._id}, reference={self._reference}, description={self._description})'


class Evidence(MessageMixin):

    def __init__(
            self,
            evidence_code: OntologyClass,
            reference: typing.Optional[ExternalReference],
    ):
        self._evidence_code = evidence_code
        self._reference = reference

    @property
    def evidence_code(self) -> OntologyClass:
        return self._evidence_code

    @evidence_code.setter
    def evidence_code(self, value: OntologyClass):
        self._evidence_code = value

    @property
    def reference(self) -> typing.Optional[ExternalReference]:
        return self._reference

    @reference.setter
    def reference(self, value: typing.Optional[ExternalReference]):
        self._reference = value

    @reference.deleter
    def reference(self):
        self._reference = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'evidence_code', 'reference'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'evidence_code' in values:
            return Evidence(
                evidence_code=extract_message_scalar('evidence_code', OntologyClass, values),
                reference=extract_message_scalar('reference', ExternalReference, values),
            )
        else:
            raise ValueError(f'Blaa')  # TODO: reword

    def __eq__(self, other):
        return isinstance(other, Evidence) \
            and self._evidence_code == other._evidence_code \
            and self._reference == other._reference

    def __repr__(self):
        return f'Evidence(evidence_code={self._evidence_code}, reference={self._reference})'


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
        self._days = value

    @days.deleter
    def days(self):
        self._days = None

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


class TimeInterval(MessageMixin):

    def __init__(
            self,
            start: Timestamp,
            end: Timestamp,
    ):
        self._start = start
        self._end = end

    @property
    def start(self) -> Timestamp:
        return self._start

    @start.setter
    def start(self, value: Timestamp):
        self._start = value

    @property
    def end(self) -> Timestamp:
        return self._end

    @end.setter
    def end(self, value: Timestamp):
        self._end = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'start', 'end'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'start' in values and 'end' in values:
            return TimeInterval(
                start=extract_message_scalar('start', Timestamp, values),
                end=extract_message_scalar('end', Timestamp, values),
            )

    def __eq__(self, other):
        return isinstance(other, TimeInterval) \
            and self._start == other._start \
            and self._end == other._end

    def __repr__(self):
        return f'TimeInterval(start={self._start}, end={self._end})'


class TimeElement(MessageMixin):

    def __init__(
            self,
            gestational_age: typing.Optional[GestationalAge] = None,
            age: typing.Optional[Age] = None,
            age_range: typing.Optional[AgeRange] = None,
            ontology_class: typing.Optional[OntologyClass] = None,
            timestamp: typing.Optional[Timestamp] = None,
            interval: typing.Optional[TimeInterval] = None,
    ):
        # exactly one one-of field must be set!
        one_ofs = (gestational_age, age, age_range, ontology_class, timestamp, interval)
        if sum(1 for arg in one_ofs if arg is not None) != 1:
            # TODO - better error
            raise ValueError('Some error happened here!')
        if gestational_age is not None:
            self._discriminant = 6
            self._val = gestational_age
        elif age is not None:
            self._discriminant = 1
            self._val = age
        elif age_range is not None:
            self._discriminant = 2
            self._val = age_range
        elif ontology_class is not None:
            self._discriminant = 3
            self._val = ontology_class
        elif timestamp is not None:
            self._discriminant = 4
            self._val = timestamp
        elif interval is not None:
            self._discriminant = 5
            self._val = interval
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
    def ontology_class(self) -> OntologyClass:
        return self._val if self._discriminant == 3 else None

    @ontology_class.setter
    def ontology_class(self, value: OntologyClass):
        self._discriminant = 3
        self._val = value

    @property
    def timestamp(self) -> Timestamp:
        return self._val if self._discriminant == 4 else None

    @timestamp.setter
    def timestamp(self, value: Timestamp):
        self._discriminant = 4
        self._val = value

    @property
    def interval(self) -> Timestamp:
        return self._val if self._discriminant == 5 else None

    @interval.setter
    def interval(self, value: TimeInterval):
        self._discriminant = 5
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
        return 'gestational_age', 'age', 'age_range', 'ontology_class', 'timestamp', 'interval'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if len(values) != 1:
            raise ValueError('Should only have one key!')  # TODO: better wording
        if 'gestational_age' in values:
            return TimeElement(gestational_age=GestationalAge.from_dict(values['gestational_age']))
        elif 'age' in values:
            return TimeElement(age=Age.from_dict(values['age']))
        elif 'age_range' in values:
            return TimeElement(age_range=AgeRange.from_dict(values['age_range']))
        elif 'ontology_class' in values:
            return TimeElement(ontology_class=OntologyClass.from_dict(values['ontology_class']))
        elif 'timestamp' in values:
            return TimeElement(timestamp=Timestamp.from_dict(values['timestamp']))
        elif 'interval' in values:
            return TimeElement(interval=TimeInterval.from_dict(values['interval']))
        else:
            raise ValueError('Bug')  # TODO: better message

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


class Procedure(MessageMixin):

    def __init__(
            self,
            code: OntologyClass,
            body_site: typing.Optional[OntologyClass],
            performed: typing.Optional[TimeElement],
    ):
        self._code = code
        self._body_site = body_site
        self._performed = performed

    @property
    def code(self) -> OntologyClass:
        return self._code

    @code.setter
    def code(self, value: OntologyClass):
        self._code = value

    @property
    def body_site(self) -> typing.Optional[OntologyClass]:
        return self._body_site

    @body_site.setter
    def body_site(self, value: typing.Optional[OntologyClass]):
        self._body_site = value

    @body_site.deleter
    def body_site(self):
        self._body_site = None

    @property
    def performed(self) -> typing.Optional[TimeElement]:
        return self._performed

    @performed.setter
    def performed(self, value: typing.Optional[TimeElement]):
        self._performed = value

    @performed.deleter
    def performed(self):
        self._performed = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'code', 'body_site', 'performed'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'code' in values:
            return Procedure(
                code=extract_message_scalar('code', OntologyClass, values),
                body_site=extract_message_scalar('body_site', OntologyClass, values),
                performed=extract_message_scalar('performed', TimeElement, values),
            )
        else:
            raise ValueError('Bug')  # TODO: reword

    def __eq__(self, other):
        return isinstance(other, Procedure) \
            and self._code == other._code \
            and self._body_site == other._body_site \
            and self._performed == other._performed

    def __repr__(self):
        return f'Procedure(code={self._code}, body_site={self._body_site}, performed={self._performed})'


class File(MessageMixin):

    def __init__(
            self,
            uri: str,
            individual_to_file_identifiers: typing.Optional[typing.Mapping[str, str]],
            file_attributes: typing.Optional[typing.Mapping[str, str]],
    ):
        self._uri = uri
        self._individual_to_file_identifiers = None if individual_to_file_identifiers is None else dict(
            individual_to_file_identifiers)
        self._file_attributes = None if file_attributes is None else dict(file_attributes)

    @property
    def uri(self) -> str:
        return self._uri

    @uri.setter
    def uri(self, value: str):
        self._uri = value

    @property
    def individual_to_file_identifiers(self) -> typing.Mapping[str, str]:
        return self._individual_to_file_identifiers

    @property
    def file_attributes(self) -> typing.Mapping[str, str]:
        return self._file_attributes

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'uri', 'individual_to_file_identifiers', 'file_attributes'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'uri' in values:
            return File(
                uri=values['uri'],
                individual_to_file_identifiers=values['individual_to_file_identifiers'],
                file_attributes=values['file_attributes'],
            )
        else:
            raise ValueError('Bug')  # TODO: reword

    def __eq__(self, other):
        return isinstance(other, File) and self._uri == other._uri \
            and self._individual_to_file_identifiers == other._individual_to_file_identifiers \
            and self._file_attributes == other._file_attributes

    def __repr__(self):
        return 'File(' \
               f'uri={self._uri},' \
               f' individual_to_file_identifiers={self._individual_to_file_identifiers}, ' \
               f' file_attributes={self._file_attributes})'
