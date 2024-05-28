import enum

import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import OntologyClass
from ._vrsatile import VariationDescriptor
from ._gene_descriptor import GeneDescriptor
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq
from ..parse import extract_oneof_scalar, extract_pb_oneof_scalar


class AcmgPathogenicityClassification(enum.Enum):
    NOT_PROVIDED = 0
    BENIGN = 1
    LIKELY_BENIGN = 2
    UNCERTAIN_SIGNIFICANCE = 3
    LIKELY_PATHOGENIC = 4
    PATHOGENIC = 5


class TherapeuticActionability(enum.Enum):
    UNKNOWN_ACTIONABILITY = 0
    NOT_ACTIONABLE = 1
    ACTIONABLE = 2


class VariantInterpretation(MessageMixin):

    def __init__(
            self,
            acmg_pathogenicity_classification: AcmgPathogenicityClassification,
            therapeutic_actionability: TherapeuticActionability,
            variation_descriptor: VariationDescriptor,
    ):
        self._acmg_pathogenicity_classification = acmg_pathogenicity_classification
        self._therapeutic_actionability = therapeutic_actionability
        self._variation_descriptor = variation_descriptor

    @property
    def acmg_pathogenicity_classification(self) -> AcmgPathogenicityClassification:
        return self._acmg_pathogenicity_classification

    @acmg_pathogenicity_classification.setter
    def acmg_pathogenicity_classification(self, value: AcmgPathogenicityClassification):
        self._acmg_pathogenicity_classification = value

    @property
    def therapeutic_actionability(self) -> TherapeuticActionability:
        return self._therapeutic_actionability

    @therapeutic_actionability.setter
    def therapeutic_actionability(self, value: TherapeuticActionability):
        self._therapeutic_actionability = value

    @property
    def variation_descriptor(self) -> VariationDescriptor:
        return self._variation_descriptor

    @variation_descriptor.setter
    def variation_descriptor(self, value: VariationDescriptor):
        self._variation_descriptor = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'acmg_pathogenicity_classification', 'therapeutic_actionability', 'variation_descriptor'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'acmg_pathogenicity_classification', 'therapeutic_actionability', 'variation_descriptor'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return VariantInterpretation(
                acmg_pathogenicity_classification=MessageMixin._extract_enum_field(
                    'acmg_pathogenicity_classification', AcmgPathogenicityClassification, values),
                therapeutic_actionability=MessageMixin._extract_enum_field(
                    'therapeutic_actionability', TherapeuticActionability, values),
                variation_descriptor=extract_message_scalar('variation_descriptor', VariationDescriptor, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.VariantInterpretation(
            acmg_pathogenicity_classification=pp202.AcmgPathogenicityClassification.Value(
                self._acmg_pathogenicity_classification.name
            ),
            therapeutic_actionability=pp202.TherapeuticActionability.Value(
                self._therapeutic_actionability.name
            ),
            variation_descriptor=self._variation_descriptor.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.VariantInterpretation

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.VariantInterpretation):
            return VariantInterpretation(
                acmg_pathogenicity_classification=AcmgPathogenicityClassification(
                    msg.acmg_pathogenicity_classification),
                therapeutic_actionability=TherapeuticActionability(msg.therapeutic_actionability),
                variation_descriptor=extract_pb_message_scalar('variation_descriptor', VariationDescriptor, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, VariantInterpretation) \
            and self._acmg_pathogenicity_classification == other._acmg_pathogenicity_classification \
            and self._therapeutic_actionability == other._therapeutic_actionability \
            and self._variation_descriptor == other._variation_descriptor

    def __repr__(self):
        return f'VariantInterpretation(acmg_pathogenicity_classification={self._acmg_pathogenicity_classification}, ' \
               f'therapeutic_actionability={self._therapeutic_actionability}, ' \
               f'variation_descriptor={self._variation_descriptor})'


class GenomicInterpretation(MessageMixin):
    _ONEOF_CALL = {
        'gene_descriptor': GeneDescriptor,
        'variant_interpretation': VariantInterpretation,
    }

    class InterpretationStatus(enum.Enum):
        UNKNOWN_STATUS = 0
        REJECTED = 1
        CANDIDATE = 2
        CONTRIBUTORY = 3
        CAUSATIVE = 4

    def __init__(
            self,
            subject_or_biosample_id: str,
            interpretation_status: InterpretationStatus,
            call: typing.Union[GeneDescriptor, VariantInterpretation],
    ):
        self._subject_or_biosample_id = subject_or_biosample_id
        self._interpretation_status = interpretation_status
        self._call = call

    @property
    def subject_or_biosample_id(self) -> str:
        return self._subject_or_biosample_id

    @subject_or_biosample_id.setter
    def subject_or_biosample_id(self, value: str):
        self._subject_or_biosample_id = value

    @property
    def interpretation_status(self) -> InterpretationStatus:
        return self._interpretation_status

    @interpretation_status.setter
    def interpretation_status(self, value: InterpretationStatus):
        self._interpretation_status = value

    @property
    def call(self) -> typing.Union[GeneDescriptor, VariantInterpretation]:
        return self._call

    @property
    def gene_descriptor(self) -> typing.Optional[GeneDescriptor]:
        return self._call if isinstance(self._call, GeneDescriptor) else None

    @gene_descriptor.setter
    def gene_descriptor(self, value: GeneDescriptor):
        self._call = value

    @property
    def variant_interpretation(self) -> typing.Optional[VariantInterpretation]:
        return self._call if isinstance(self._call, VariantInterpretation) else None

    @variant_interpretation.setter
    def variant_interpretation(self, value: VariantInterpretation):
        self._call = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'subject_or_biosample_id', 'interpretation_status', 'gene_descriptor', 'variant_interpretation'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if 'subject_or_biosample_id' in values \
                and 'interpretation_status' in values \
                and any(field in values for field in cls._ONEOF_CALL):
            return GenomicInterpretation(
                subject_or_biosample_id=values['subject_or_biosample_id'],
                interpretation_status=MessageMixin._extract_enum_field(
                    'interpretation_status', GenomicInterpretation.InterpretationStatus, values,
                ),
                call=extract_oneof_scalar(cls._ONEOF_CALL, values),
            )
        else:
            raise ValueError(
                'Missing one of required fields: '
                f'`subject_or_biosample_id, interpretation_status, gene_descriptor|variant_interpretation` in {values}'
            )

    def to_message(self) -> Message:
        msg = pp202.GenomicInterpretation(
            subject_or_biosample_id=self._subject_or_biosample_id,
            interpretation_status=pp202.GenomicInterpretation.InterpretationStatus.Value(
                self._interpretation_status.name
            ),
        )

        if isinstance(self._call, GeneDescriptor):
            msg.gene_descriptor.CopyFrom(self._call.to_message())
        elif isinstance(self._call, VariantInterpretation):
            msg.variant_interpretation.CopyFrom(self._call.to_message())
        else:
            raise ValueError('Bug')

        return msg

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.GenomicInterpretation

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return GenomicInterpretation(
                subject_or_biosample_id=msg.subject_or_biosample_id,
                interpretation_status=GenomicInterpretation.InterpretationStatus(msg.interpretation_status),
                call=extract_pb_oneof_scalar('call', cls._ONEOF_CALL, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, GenomicInterpretation) \
            and self._subject_or_biosample_id == other._subject_or_biosample_id \
            and self._interpretation_status == other._interpretation_status \
            and self._call == other._call

    def __repr__(self):
        return f'GenomicInterpretation(' \
               f'subject_or_biosample_id={self._subject_or_biosample_id}, ' \
               f'interpretation_status={self._interpretation_status}, ' \
               f'call={self._call})'


class Diagnosis(MessageMixin):

    def __init__(
            self,
            disease: OntologyClass,
            genomic_interpretations: typing.Optional[typing.Iterable[GenomicInterpretation]] = None,
    ):
        self._disease = disease
        self._genomic_interpretations = [] if genomic_interpretations is None else list(genomic_interpretations)

    @property
    def disease(self) -> OntologyClass:
        return self._disease

    @disease.setter
    def disease(self, value: OntologyClass):
        self._disease = value

    @property
    def genomic_interpretations(self) -> typing.MutableSequence[GenomicInterpretation]:
        return self._genomic_interpretations

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'disease', 'genomic_interpretations'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'disease',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Diagnosis(
                disease=extract_message_scalar('disease', OntologyClass, values),
                genomic_interpretations=extract_message_sequence(
                    'genomic_interpretations', GenomicInterpretation, values
                ),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Diagnosis(
            disease=self._disease.to_message(),
            genomic_interpretations=(gi.to_message() for gi in self._genomic_interpretations),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Diagnosis

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Diagnosis):
            return Diagnosis(
                disease=extract_pb_message_scalar('disease', OntologyClass, msg),
                genomic_interpretations=extract_pb_message_seq('genomic_interpretations', GenomicInterpretation, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Diagnosis) \
            and self._disease == other._disease \
            and self._genomic_interpretations == other._genomic_interpretations

    def __repr__(self):
        return f'Diagnosis(' \
               f'disease={self._disease}' \
               f'genomic_interpretations={self._genomic_interpretations})'


class Interpretation(MessageMixin):
    class ProgressStatus(enum.Enum):
        UNKNOWN_PROGRESS = 0
        IN_PROGRESS = 1
        COMPLETED = 2
        SOLVED = 3
        UNSOLVED = 4

    def __init__(
            self,
            id: str,
            progress_status: ProgressStatus,
            diagnosis: typing.Optional[Diagnosis] = None,
            summary: typing.Optional[str] = None,
    ):
        self._id = id
        self._progress_status = progress_status
        self._diagnosis = diagnosis
        self._summary = summary

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def progress_status(self) -> ProgressStatus:
        return self._progress_status

    @progress_status.setter
    def progress_status(self, value: ProgressStatus):
        self._progress_status = value

    @property
    def diagnosis(self) -> typing.Optional[Diagnosis]:
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, value: Diagnosis):
        self._diagnosis = value

    @diagnosis.deleter
    def diagnosis(self):
        self._diagnosis = None

    @property
    def summary(self) -> typing.Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: str):
        self._summary = value

    @summary.deleter
    def summary(self):
        self._summary = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'progress_status', 'diagnosis', 'summary'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'id', 'progress_status',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Interpretation(
                id=values['id'],
                progress_status=MessageMixin._extract_enum_field('progress_status', Interpretation.ProgressStatus,
                                                                 values),
                diagnosis=extract_message_scalar('diagnosis', Diagnosis, values),
                summary=MessageMixin._extract_optional_field('summary', values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        i = pp202.Interpretation(
            id=self._id,
            progress_status=pp202.Interpretation.ProgressStatus.Value(self._progress_status.name),
        )

        if self._diagnosis is not None:
            i.diagnosis.CopyFrom(self._diagnosis.to_message())

        if self._summary is not None:
            i.summary = self._summary

        return i

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Interpretation

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Interpretation):
            return Interpretation(
                id=msg.id,
                progress_status=Interpretation.ProgressStatus(msg.progress_status),
                diagnosis=extract_pb_message_scalar('diagnosis', Diagnosis, msg),
                summary=None if msg.summary == '' else msg.summary,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Interpretation) \
            and self._id == other._id \
            and self._progress_status == other._progress_status \
            and self._diagnosis == other._diagnosis \
            and self._summary == other._summary

    def __repr__(self):
        return f'Interpretation(' \
               f'id={self._id}, ' \
               f'progress_status={self._progress_status}, ' \
               f'diagnosis={self._diagnosis}, ' \
               f'summary={self._summary})'
