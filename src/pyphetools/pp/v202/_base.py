import typing

import phenopackets as pp202
from google.protobuf.message import Message

from .._api import MessageMixin
from .._timestamp import Timestamp
from ..parse import extract_message_scalar, extract_pb_message_scalar, extract_oneof_scalar, extract_pb_oneof_scalar


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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'id', 'label'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return OntologyClass(
                id=values['id'],
                label=values['label'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.OntologyClass(
            id=self._id,
            label=self._label,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.OntologyClass

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.OntologyClass):
            return OntologyClass(
                id=msg.id,
                label=msg.label,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return ()

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return ExternalReference(
                id=MessageMixin._extract_optional_field('id', values),
                reference=MessageMixin._extract_optional_field('reference', values),
                description=MessageMixin._extract_optional_field('description', values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.ExternalReference(
            id=None if self._id is None else self._id,
            reference=None if self._reference is None else self._reference,
            description=None if self._description is None else self._description,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.ExternalReference

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.ExternalReference):
            return ExternalReference(
                id=None if msg.id == '' else msg.id,
                reference=None if msg.reference == '' else msg.reference,
                description=None if msg.description == '' else msg.description,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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
            reference: typing.Optional[ExternalReference] = None,
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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'evidence_code',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Evidence(
                evidence_code=extract_message_scalar('evidence_code', OntologyClass, values),
                reference=extract_message_scalar('reference', ExternalReference, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Evidence(
            evidence_code=self._evidence_code.to_message(),
            reference=self._reference.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Evidence

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Evidence):
            return Evidence(
                evidence_code=extract_pb_message_scalar('evidence_code', OntologyClass, msg),
                reference=extract_pb_message_scalar('reference', ExternalReference, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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
            days: typing.Optional[int] = None,
    ):
        # TODO: validate
        self._weeks = weeks
        self._days = days

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
    def field_names() -> typing.Iterable[str]:
        return 'weeks', 'days',

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'weeks',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            weeks = values['weeks']
            days = values['days'] if 'days' in values else None
            return GestationalAge(
                weeks=weeks,
                days=days,
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.GestationalAge(
            weeks=self._weeks,
            days=self._days,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.GestationalAge

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.GestationalAge):
            return GestationalAge(
                weeks=msg.weeks,
                days=msg.days,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'iso8601duration',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Age(iso8601duration=values['iso8601duration'])
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Age(
            iso8601duration=self._iso8601duration,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Age

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Age):
            return Age(
                iso8601duration=msg.iso8601duration,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'start', 'end'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return AgeRange(
                start=Age.from_dict(values['start']),
                end=Age.from_dict(values['end']),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.AgeRange(
            start=self._start.to_message(),
            end=self._end.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.AgeRange

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.AgeRange):
            return AgeRange(
                start=extract_pb_message_scalar('start', Age, msg),
                end=extract_pb_message_scalar('end', Age, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'start', 'end'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return TimeInterval(
                start=Timestamp.from_str(values['start']),
                end=Timestamp.from_str(values['end']),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.TimeInterval(
            start=self._start.to_message(),
            end=self._end.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.TimeInterval

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.TimeInterval):
            return TimeInterval(
                start=extract_pb_message_scalar('start', Timestamp, msg),
                end=extract_pb_message_scalar('end', Timestamp, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, TimeInterval) \
            and self._start == other._start \
            and self._end == other._end

    def __repr__(self):
        return f'TimeInterval(start={self._start}, end={self._end})'


class TimeElement(MessageMixin):
    """
    TODO: better description
    """
    _ONEOF_ELEMENT = {
        'gestational_age': GestationalAge, 'age': Age, 'age_range': AgeRange,
        'ontology_class': OntologyClass, 'timestamp': Timestamp, 'interval': TimeInterval,
    }

    def __init__(
            self,
            element: typing.Union[GestationalAge, Age, AgeRange, OntologyClass, Timestamp, TimeInterval]
    ):
        self._element = element

    @property
    def element(self) -> typing.Union[GestationalAge, Age, AgeRange, OntologyClass, Timestamp, TimeInterval]:
        return self._element

    @property
    def age(self) -> typing.Optional[Age]:
        return self._element if isinstance(self._element, Age) else None

    @age.setter
    def age(self, value: Age):
        self._element = value

    @property
    def age_range(self) -> typing.Optional[AgeRange]:
        return self._element if isinstance(self._element, AgeRange) else None

    @age_range.setter
    def age_range(self, value: AgeRange):
        self._element = value

    @property
    def ontology_class(self) -> OntologyClass:
        return self._element if isinstance(self._element, OntologyClass) else None

    @ontology_class.setter
    def ontology_class(self, value: OntologyClass):
        self._element = value

    @property
    def timestamp(self) -> Timestamp:
        return self._element if isinstance(self._element, Timestamp) else None

    @timestamp.setter
    def timestamp(self, value: Timestamp):
        self._element = value

    @property
    def interval(self) -> TimeInterval:
        return self._element if isinstance(self._element, TimeInterval) else None

    @interval.setter
    def interval(self, value: TimeInterval):
        self._element = value

    @property
    def gestational_age(self) -> typing.Optional[GestationalAge]:
        return self._element if isinstance(self._element, GestationalAge) else None

    @gestational_age.setter
    def gestational_age(self, value: GestationalAge):
        self._element = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'gestational_age', 'age', 'age_range', 'ontology_class', 'timestamp', 'interval'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(field in values for field in cls._ONEOF_ELEMENT):
            return TimeElement(
                element=extract_oneof_scalar(cls._ONEOF_ELEMENT, values)
            )
        else:
            raise ValueError(
                f'Missing one of required fields: '
                f'`{"|".join(cls._ONEOF_ELEMENT)}`: {values}'
            )

    def to_message(self) -> Message:
        te = pp202.TimeElement()

        val = self._element.to_message()
        if isinstance(self._element, Age):
            te.age.CopyFrom(val)
        elif isinstance(self._element, AgeRange):
            te.age_range.CopyFrom(val)
        elif isinstance(self._element, OntologyClass):
            te.ontology_class.CopyFrom(val)
        elif isinstance(self._element, Timestamp):
            te.timestamp.CopyFrom(val)
        elif isinstance(self._element, TimeInterval):
            te.interval.CopyFrom(val)
        elif isinstance(self._element, GestationalAge):
            te.gestational_age.CopyFrom(val)
        else:
            raise ValueError('Bug')

        return te

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.TimeElement

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return TimeElement(
                element=extract_pb_oneof_scalar(
                    'element',
                    {
                        'gestational_age': GestationalAge, 'age': Age, 'age_range': AgeRange,
                        'ontology_class': OntologyClass, 'timestamp': Timestamp, 'interval': TimeInterval,
                    }, msg)
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, TimeElement) and self._element == other._element

    def __repr__(self):
        return f'TimeElement(element={self._element})'


class Procedure(MessageMixin):

    def __init__(
            self,
            code: OntologyClass,
            body_site: typing.Optional[OntologyClass] = None,
            performed: typing.Optional[TimeElement] = None,
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

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'code',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Procedure(
                code=extract_message_scalar('code', OntologyClass, values),
                body_site=extract_message_scalar('body_site', OntologyClass, values),
                performed=extract_message_scalar('performed', TimeElement, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        procedure = pp202.Procedure(
            code=self._code.to_message(),
        )

        if self._body_site is not None:
            procedure.body_site.CopyFrom(self._body_site.to_message())

        if self._performed is not None:
            procedure.performed.CopyFrom(self._performed.to_message())

        return procedure

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Procedure

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Procedure):
            return Procedure(
                code=extract_pb_message_scalar('code', OntologyClass, msg),
                body_site=extract_pb_message_scalar('body_site', OntologyClass, msg),
                performed=extract_pb_message_scalar('performed', TimeElement, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

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
            individual_to_file_identifiers: typing.Optional[typing.Mapping[str, str]] = None,
            file_attributes: typing.Optional[typing.Mapping[str, str]] = None,
    ):
        self._uri = uri
        self._individual_to_file_identifiers = dict() \
            if individual_to_file_identifiers is None \
            else dict(individual_to_file_identifiers)
        self._file_attributes = dict() if file_attributes is None else dict(file_attributes)

    @property
    def uri(self) -> str:
        return self._uri

    @uri.setter
    def uri(self, value: str):
        self._uri = value

    @property
    def individual_to_file_identifiers(self) -> typing.MutableMapping[str, str]:
        return self._individual_to_file_identifiers

    @property
    def file_attributes(self) -> typing.MutableMapping[str, str]:
        return self._file_attributes

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'uri', 'individual_to_file_identifiers', 'file_attributes'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'uri',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return File(
                uri=values['uri'],
                individual_to_file_identifiers=values['individual_to_file_identifiers'],
                file_attributes=values['file_attributes'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        file = pp202.File(uri=self._uri)
        for k, v in self._individual_to_file_identifiers.items():
            file.individual_to_file_identifiers[k] = v

        for k, v in self._file_attributes.items():
            file.file_attributes[k] = v

        return file

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.File

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.File):
            return File(
                uri=msg.uri,
                individual_to_file_identifiers=msg.individual_to_file_identifiers,
                file_attributes=msg.file_attributes,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, File) and self._uri == other._uri \
            and self._individual_to_file_identifiers == other._individual_to_file_identifiers \
            and self._file_attributes == other._file_attributes

    def __repr__(self):
        return 'File(' \
               f'uri={self._uri},' \
               f' individual_to_file_identifiers={self._individual_to_file_identifiers},' \
               f' file_attributes={self._file_attributes})'
