import enum

import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import OntologyClass
from ._vrsatile import VariationDescriptor
from ._gene_descriptor import GeneDescriptor
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


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

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        pass

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        pass

    def to_message(self) -> Message:
        pass

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.VariantInterpretation

    @classmethod
    def from_message(cls, msg: Message):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass


class GenomicInterpretation(MessageMixin):

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

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        pass

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        pass

    def to_message(self) -> Message:
        pass

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.GenomicInterpretation

    @classmethod
    def from_message(cls, msg: Message):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass


class Diagnosis(MessageMixin):

    def __init__(
            self,
            disease: OntologyClass,
            genomic_interpretations: typing.Optional[typing.Iterable[GenomicInterpretation]] = None,
    ):
        self._disease = disease
        self._genomic_interpretations = [] if genomic_interpretations is None else list(genomic_interpretations)

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        pass

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        pass

    def to_message(self) -> Message:
        pass

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Diagnosis

    @classmethod
    def from_message(cls, msg: Message):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass


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

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        pass

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        pass

    def to_message(self) -> Message:
        pass

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Interpretation

    @classmethod
    def from_message(cls, msg: Message):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass
