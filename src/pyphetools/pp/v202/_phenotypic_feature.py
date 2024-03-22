import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import OntologyClass, TimeElement, Evidence
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class PhenotypicFeature(MessageMixin):

    def __init__(
            self,
            type: OntologyClass,
            excluded: bool = False,
            description: typing.Optional[str] = None,
            severity: typing.Optional[OntologyClass] = None,
            modifiers: typing.Optional[typing.Iterable[OntologyClass]] = None,
            onset: typing.Optional[TimeElement] = None,
            resolution: typing.Optional[TimeElement] = None,
            evidence: typing.Optional[typing.Iterable[Evidence]] = None,
    ):
        self._type = type
        self._excluded = excluded
        self._description = description
        self._severity = severity
        self._modifiers = [] if modifiers is None else list(modifiers)
        self._onset = onset
        self._resolution = resolution
        self._evidence = [] if evidence is None else list(evidence)

    @property
    def type(self) -> OntologyClass:
        return self._type

    @type.setter
    def type(self, value: OntologyClass):
        self._type = value

    @property
    def excluded(self) -> bool:
        return self._excluded

    @excluded.setter
    def excluded(self, value: bool):
        self._excluded = value

    @property
    def description(self) -> typing.Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @description.deleter
    def description(self):
        self._description = None

    @property
    def severity(self) -> typing.Optional[OntologyClass]:
        return self._severity

    @severity.setter
    def severity(self, value: OntologyClass):
        self._severity = value

    @severity.deleter
    def severity(self):
        self._severity = None

    @property
    def modifiers(self) -> typing.MutableSequence[OntologyClass]:
        return self._modifiers

    @property
    def onset(self) -> typing.Optional[TimeElement]:
        return self._onset

    @onset.setter
    def onset(self, value: TimeElement):
        self._onset = value

    @onset.deleter
    def onset(self):
        self._onset = None

    @property
    def resolution(self) -> typing.Optional[TimeElement]:
        return self._resolution

    @resolution.setter
    def resolution(self, value: TimeElement):
        self._resolution = value

    @resolution.deleter
    def resolution(self):
        self._resolution = None

    @property
    def evidence(self) -> typing.MutableSequence[Evidence]:
        return self._evidence

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'type', 'excluded', 'description', 'severity', 'modifiers', 'onset', 'resolution', 'evidence'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'type',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return PhenotypicFeature(
                type=extract_message_scalar('type', OntologyClass, values),
                excluded=values['excluded'] if 'excluded' in values else False,
                description=values['description'] if 'description' in values else None,
                severity=extract_message_scalar('severity', OntologyClass, values),
                modifiers=extract_message_sequence('modifiers', OntologyClass, values),
                onset=extract_message_scalar('onset', TimeElement, values),
                resolution=extract_message_scalar('resolution', TimeElement, values),
                evidence=extract_message_sequence('evidence', Evidence, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        pf = pp202.PhenotypicFeature(
            type=self._type.to_message(), excluded=self._excluded,
        )

        if self._description is not None:
            pf.description = self._description

        if self._severity is not None:
            pf.severity.CopyFrom(self._severity.to_message())

        pf.modifiers.extend(m.to_message() for m in self._modifiers)

        if self._onset is not None:
            pf.onset.CopyFrom(self._onset.to_message())

        if self._resolution is not None:
            pf.resolution.CopyFrom(self._resolution.to_message())

        pf.evidence.extend(e.to_message() for e in self._evidence)

        return pf

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.PhenotypicFeature

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return PhenotypicFeature(
                type=extract_pb_message_scalar('type', OntologyClass, msg),
                excluded=msg.excluded,
                description=None if msg.description == '' else msg.description,
                severity=extract_pb_message_scalar('severity', OntologyClass, msg),
                modifiers=extract_pb_message_seq('modifiers', OntologyClass, msg),
                onset=extract_pb_message_scalar('onset', TimeElement, msg),
                resolution=extract_pb_message_scalar('resolution', TimeElement, msg),
                evidence=extract_pb_message_seq('evidence', Evidence, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, PhenotypicFeature) \
            and self._type == other._type \
            and self._excluded == other._excluded \
            and self._description == other._description \
            and self._severity == other._severity \
            and self._modifiers == other._modifiers \
            and self._onset == other._onset \
            and self._resolution == other._resolution \
            and self._evidence == other._evidence

    def __repr__(self):
        return (f'PhenotypicFeature(type={self._type}, '
                f'excluded={self._excluded}, '
                f'description={self._description}, '
                f'severity={self._severity}, '
                f'modifiers={self._modifiers}, '
                f'onset={self._onset}, '
                f'resolution={self._resolution}, '
                f'evidence={self._evidence})')
