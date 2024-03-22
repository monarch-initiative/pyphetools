import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import OntologyClass, TimeElement
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class Disease(MessageMixin):

    def __init__(
            self,
            term: OntologyClass,
            excluded: bool = False,
            onset: typing.Optional[TimeElement] = None,
            resolution: typing.Optional[TimeElement] = None,
            disease_stage: typing.Optional[typing.Iterable[OntologyClass]] = None,
            clinical_tnm_finding: typing.Optional[typing.Iterable[OntologyClass]] = None,
            primary_site: typing.Optional[OntologyClass] = None,
            laterality: typing.Optional[OntologyClass] = None,
    ):
        self._term = term
        self._excluded = excluded
        self._onset = onset
        self._resolution = resolution
        self._disease_stage = [] if disease_stage is None else list(disease_stage)
        self._clinical_tnm_finding = [] if clinical_tnm_finding is None else list(clinical_tnm_finding)
        self._primary_site = primary_site
        self._laterality = laterality

    @property
    def term(self) -> OntologyClass:
        return self._term

    @term.setter
    def term(self, value: OntologyClass):
        self._term = value

    @property
    def excluded(self) -> bool:
        return self._excluded

    @excluded.setter
    def excluded(self, value: bool):
        self._excluded = value

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
    def disease_stage(self) -> typing.MutableSequence[OntologyClass]:
        return self._disease_stage

    @property
    def clinical_tnm_finding(self) -> typing.MutableSequence[OntologyClass]:
        return self._clinical_tnm_finding

    @property
    def primary_site(self) -> typing.Optional[OntologyClass]:
        return self._primary_site

    @primary_site.setter
    def primary_site(self, value: OntologyClass):
        self._primary_site = value

    @primary_site.deleter
    def primary_site(self):
        self._primary_site = None

    @property
    def laterality(self) -> typing.Optional[OntologyClass]:
        return self._laterality

    @laterality.setter
    def laterality(self, value: OntologyClass):
        self._laterality = value

    @laterality.deleter
    def laterality(self):
        self._laterality = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'term', 'excluded', 'onset', 'resolution', 'disease_stage', 'clinical_tnm_finding', 'primary_site', 'laterality'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'term',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Disease(
                term=extract_message_scalar('term', OntologyClass, values),
                excluded=values['excluded'] if 'excluded' in values else False,
                onset=extract_message_scalar('onset', TimeElement, values),
                resolution=extract_message_scalar('resolution', TimeElement, values),
                disease_stage=extract_message_sequence('disease_stage', OntologyClass, values),
                clinical_tnm_finding=extract_message_sequence('clinical_tnm_finding', OntologyClass, values),
                primary_site=extract_message_scalar('primary_site', OntologyClass, values),
                laterality=extract_message_scalar('laterality', OntologyClass, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        disease = pp202.Disease(term=self._term.to_message(), excluded=self._excluded)

        if self._onset is not None:
            disease.onset.CopyFrom(self._onset.to_message())

        if self._resolution is not None:
            disease.resolution.CopyFrom(self._resolution.to_message())

        disease.disease_stage.extend(ds.to_message() for ds in self._disease_stage)
        disease.clinical_tnm_finding.extend(tnm.to_message() for tnm in self._clinical_tnm_finding)

        if self._primary_site is not None:
            disease.primary_site.CopyFrom(self._primary_site.to_message())

        if self._laterality is not None:
            disease.laterality.CopyFrom(self._laterality.to_message())

        return disease

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Disease

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Disease(
                term=extract_pb_message_scalar('term', OntologyClass, msg),
                excluded=msg.excluded,
                onset=extract_pb_message_scalar('onset', TimeElement, msg),
                resolution=extract_pb_message_scalar('resolution', TimeElement, msg),
                disease_stage=extract_pb_message_seq('disease_stage', OntologyClass, msg),
                clinical_tnm_finding=extract_pb_message_seq('clinical_tnm_finding', OntologyClass, msg),
                primary_site=extract_pb_message_scalar('primary_site', OntologyClass, msg),
                laterality=extract_pb_message_scalar('laterality', OntologyClass, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Disease) \
            and self._term == other._term \
            and self._excluded == other._excluded \
            and self._onset == other._onset \
            and self._resolution == other._resolution \
            and self._disease_stage == other._disease_stage \
            and self._clinical_tnm_finding == other._clinical_tnm_finding \
            and self._primary_site == other._primary_site \
            and self._laterality == other._laterality

    def __repr__(self):
        return (f'Disease(term={self._term}, '
                f'excluded={self._excluded}, '
                f'onset={self._onset}, '
                f'resolution={self._resolution}, '
                f'disease_stage={self._disease_stage}, '
                f'clinical_tnm_finding={self._clinical_tnm_finding}, '
                f'primary_site={self._primary_site}, '
                f'laterality={self._laterality}'
                ')')
