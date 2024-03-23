import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import OntologyClass, TimeElement, File, Procedure
from ._measurement import Measurement
from ._phenotypic_feature import PhenotypicFeature
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class Biosample(MessageMixin):

    def __init__(
            self,
            id: str,
            individual_id: typing.Optional[str] = None,
            derived_from_id: typing.Optional[str] = None,
            description: typing.Optional[str] = None,
            sampled_tissue: typing.Optional[OntologyClass] = None,
            sample_type: typing.Optional[OntologyClass] = None,
            phenotypic_features: typing.Optional[typing.Iterable[PhenotypicFeature]] = None,
            measurements: typing.Optional[typing.Iterable[Measurement]] = None,
            taxonomy: typing.Optional[OntologyClass] = None,
            time_of_collection: typing.Optional[TimeElement] = None,
            histological_diagnosis: typing.Optional[OntologyClass] = None,
            tumor_progression: typing.Optional[OntologyClass] = None,
            tumor_grade: typing.Optional[OntologyClass] = None,
            pathological_stage: typing.Optional[OntologyClass] = None,
            pathological_tnm_finding: typing.Optional[typing.Iterable[OntologyClass]] = None,
            diagnostic_markers: typing.Optional[typing.Iterable[OntologyClass]] = None,
            procedure: typing.Optional[Procedure] = None,
            files: typing.Optional[typing.Iterable[File]] = None,
            material_sample: typing.Optional[OntologyClass] = None,
            sample_processing: typing.Optional[OntologyClass] = None,
            sample_storage: typing.Optional[OntologyClass] = None,
    ):
        self._id = id
        self._individual_id = individual_id
        self._derived_from_id = derived_from_id
        self._description = description
        self._sampled_tissue = sampled_tissue
        self._sample_type = sample_type
        self._phenotypic_features = [] if phenotypic_features is None else list(phenotypic_features)
        self._measurements = [] if measurements is None else list(measurements)
        self._taxonomy = taxonomy
        self._time_of_collection = time_of_collection
        self._histological_diagnosis = histological_diagnosis
        self._tumor_progression = tumor_progression
        self._tumor_grade = tumor_grade
        self._pathological_stage = pathological_stage
        self._pathological_tnm_finding = [] if pathological_tnm_finding is None else list(pathological_tnm_finding)
        self._diagnostic_markers = [] if diagnostic_markers is None else list(diagnostic_markers)
        self._procedure = procedure
        self._files = [] if files is None else list(files)
        self._material_sample = material_sample
        self._sample_processing = sample_processing
        self._sample_storage = sample_storage

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def individual_id(self) -> typing.Optional[str]:
        return self._individual_id

    @individual_id.setter
    def individual_id(self, value: str):
        self._individual_id = value

    @individual_id.deleter
    def individual_id(self):
        self._individual_id = None

    @property
    def derived_from_id(self) -> typing.Optional[str]:
        return self._derived_from_id

    @derived_from_id.setter
    def derived_from_id(self, value: str):
        self._derived_from_id = value

    @derived_from_id.deleter
    def derived_from_id(self):
        self._derived_from_id = None

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
    def sampled_tissue(self) -> typing.Optional[OntologyClass]:
        return self._sampled_tissue

    @sampled_tissue.setter
    def sampled_tissue(self, value: OntologyClass):
        self._sampled_tissue = value

    @sampled_tissue.deleter
    def sampled_tissue(self):
        self._sampled_tissue = None

    @property
    def sample_type(self) -> typing.Optional[OntologyClass]:
        return self._sample_type

    @sample_type.setter
    def sample_type(self, value: OntologyClass):
        self._sample_type = value

    @sample_type.deleter
    def sample_type(self):
        self._sample_type = None

    @property
    def phenotypic_features(self) -> typing.MutableSequence[PhenotypicFeature]:
        return self._phenotypic_features

    @property
    def measurements(self) -> typing.MutableSequence[Measurement]:
        return self._measurements

    @property
    def taxonomy(self) -> typing.Optional[OntologyClass]:
        return self._taxonomy

    @taxonomy.setter
    def taxonomy(self, value: OntologyClass):
        self._taxonomy = value

    @taxonomy.deleter
    def taxonomy(self):
        self._taxonomy = None

    @property
    def time_of_collection(self) -> typing.Optional[TimeElement]:
        return self._time_of_collection

    @time_of_collection.setter
    def time_of_collection(self, value: TimeElement):
        self._time_of_collection = value

    @time_of_collection.deleter
    def time_of_collection(self):
        self._time_of_collection = None

    @property
    def histological_diagnosis(self) -> typing.Optional[OntologyClass]:
        return self._histological_diagnosis

    @histological_diagnosis.setter
    def histological_diagnosis(self, value: OntologyClass):
        self._histological_diagnosis = value

    @histological_diagnosis.deleter
    def histological_diagnosis(self):
        self._histological_diagnosis = None

    @property
    def tumor_progression(self) -> typing.Optional[OntologyClass]:
        return self._tumor_progression

    @tumor_progression.setter
    def tumor_progression(self, value: OntologyClass):
        self._tumor_progression = value

    @tumor_progression.deleter
    def tumor_progression(self):
        self._tumor_progression = None

    @property
    def tumor_grade(self) -> typing.Optional[OntologyClass]:
        return self._tumor_grade

    @tumor_grade.setter
    def tumor_grade(self, value: OntologyClass):
        self._tumor_grade = value

    @tumor_grade.deleter
    def tumor_grade(self):
        self._tumor_grade = None

    @property
    def pathological_stage(self) -> typing.Optional[OntologyClass]:
        return self._pathological_stage

    @pathological_stage.setter
    def pathological_stage(self, value: OntologyClass):
        self._pathological_stage = value

    @pathological_stage.deleter
    def pathological_stage(self):
        self._pathological_stage = None

    @property
    def pathological_tnm_finding(self) -> typing.MutableSequence[OntologyClass]:
        return self._pathological_tnm_finding

    @property
    def diagnostic_markers(self) -> typing.MutableSequence[OntologyClass]:
        return self._diagnostic_markers

    @property
    def procedure(self) -> typing.Optional[Procedure]:
        return self._procedure

    @procedure.setter
    def procedure(self, value: Procedure):
        self._procedure = value

    @procedure.deleter
    def procedure(self):
        self._procedure = None

    @property
    def files(self) -> typing.MutableSequence[File]:
        return self._files

    @property
    def material_sample(self) -> typing.Optional[OntologyClass]:
        return self._material_sample

    @material_sample.setter
    def material_sample(self, value: OntologyClass):
        self._material_sample = value

    @material_sample.deleter
    def material_sample(self):
        self._material_sample = None

    @property
    def sample_processing(self) -> typing.Optional[OntologyClass]:
        return self._sample_processing

    @sample_processing.setter
    def sample_processing(self, value: OntologyClass):
        self._sample_processing = value

    @sample_processing.deleter
    def sample_processing(self):
        self._sample_processing = None

    @property
    def sample_storage(self) -> typing.Optional[OntologyClass]:
        return self._sample_storage

    @sample_storage.setter
    def sample_storage(self, value: OntologyClass):
        self._sample_storage = value

    @sample_storage.deleter
    def sample_storage(self):
        self._sample_storage = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return (
            'id', 'individual_id', 'derived_from_id', 'description', 'sampled_tissue', 'sample_type',
            'phenotypic_features', 'measurements',
            'taxonomy', 'time_of_collection', 'histological_diagnosis', 'tumor_progression', 'tumor_grade',
            'pathological_stage', 'pathological_tnm_finding', 'diagnostic_markers', 'procedure',
            'files', 'material_sample', 'sample_processing', 'sample_storage',
        )

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'id',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Biosample(
                id=values['id'],
                individual_id=values['individual_id'] if 'individual_id' in values else None,
                derived_from_id=values['derived_from_id'] if 'derived_from_id' in values else None,
                description=values['description'] if 'description' in values else None,
                sampled_tissue=extract_message_scalar('sampled_tissue', OntologyClass, values),
                sample_type=extract_message_scalar('sample_type', OntologyClass, values),
                phenotypic_features=extract_message_sequence('phenotypic_features', PhenotypicFeature, values),
                measurements=extract_message_sequence('measurements', Measurement, values),
                taxonomy=extract_message_scalar('taxonomy', OntologyClass, values),
                time_of_collection=extract_message_scalar('time_of_collection', OntologyClass, values),
                histological_diagnosis=extract_message_scalar('histological_diagnosis', OntologyClass, values),
                tumor_progression=extract_message_scalar('tumor_progression', OntologyClass, values),
                tumor_grade=extract_message_scalar('tumor_grade', OntologyClass, values),
                pathological_stage=extract_message_scalar('pathological_stage', OntologyClass, values),
                pathological_tnm_finding=extract_message_sequence('pathological_tnm_finding', OntologyClass, values),
                diagnostic_markers=extract_message_sequence('diagnostic_markers', OntologyClass, values),
                procedure=extract_message_scalar('procedure', Procedure, values),
                files=extract_message_sequence('files', File, values),
                material_sample=extract_message_scalar('material_sample', OntologyClass, values),
                sample_processing=extract_message_scalar('sample_processing', OntologyClass, values),
                sample_storage=extract_message_scalar('sample_storage', OntologyClass, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        biosample = pp202.Biosample(id=self._id)

        if self._individual_id is not None:
            biosample.individual_id = self._individual_id

        if self._derived_from_id is not None:
            biosample.derived_from_id = self._derived_from_id

        if self._description is not None:
            biosample.description = self._description

        # Set optional compound singular & sequence fields
        for name in (
                'sampled_tissue', 'sample_type', 'phenotypic_features', 'measurements',
                'taxonomy', 'time_of_collection', 'histological_diagnosis', 'tumor_progression', 'tumor_grade',
                'pathological_stage', 'pathological_tnm_finding', 'diagnostic_markers', 'procedure',
                'files', 'material_sample', 'sample_processing', 'sample_storage',
        ):
            field = getattr(self, name)
            if field is not None:
                target = getattr(biosample, name)
                if isinstance(field, typing.List):
                    target.extend(item.to_message() for item in field)
                else:
                    target.CopyFrom(field.to_message())

        return biosample

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Biosample

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Biosample(
                id=msg.id,
                individual_id=None if msg.individual_id == '' else msg.individual_id,
                derived_from_id=None if msg.derived_from_id == '' else msg.derived_from_id,
                description=None if msg.description == '' else msg.description,
                sampled_tissue=extract_pb_message_scalar('sampled_tissue', OntologyClass, msg),
                sample_type=extract_pb_message_scalar('sample_type', OntologyClass, msg),
                phenotypic_features=extract_pb_message_seq('phenotypic_features', PhenotypicFeature, msg),
                measurements=extract_pb_message_seq('measurements', Measurement, msg),
                taxonomy=extract_pb_message_scalar('taxonomy', OntologyClass, msg),
                time_of_collection=extract_pb_message_scalar('time_of_collection', OntologyClass, msg),
                histological_diagnosis=extract_pb_message_scalar('histological_diagnosis', OntologyClass, msg),
                tumor_progression=extract_pb_message_scalar('tumor_progression', OntologyClass, msg),
                tumor_grade=extract_pb_message_scalar('tumor_grade', OntologyClass, msg),
                pathological_stage=extract_pb_message_scalar('pathological_stage', OntologyClass, msg),
                pathological_tnm_finding=extract_pb_message_seq('pathological_tnm_finding', OntologyClass, msg),
                diagnostic_markers=extract_pb_message_seq('diagnostic_markers', OntologyClass, msg),
                procedure=extract_pb_message_scalar('procedure', Procedure, msg),
                files=extract_pb_message_seq('files', File, msg),
                material_sample=extract_pb_message_scalar('material_sample', OntologyClass, msg),
                sample_processing=extract_pb_message_scalar('sample_processing', OntologyClass, msg),
                sample_storage=extract_pb_message_scalar('sample_storage', OntologyClass, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Biosample) \
            and self._id == other._id \
            and self._individual_id == other._individual_id \
            and self._derived_from_id == other._derived_from_id \
            and self._description == other._description \
            and self._sampled_tissue == other._sampled_tissue \
            and self._sample_type == other._sample_type \
            and self._phenotypic_features == other._phenotypic_features \
            and self._measurements == other._measurements \
            and self._taxonomy == other._taxonomy \
            and self._time_of_collection == other._time_of_collection \
            and self._histological_diagnosis == other._histological_diagnosis \
            and self._tumor_progression == other._tumor_progression \
            and self._tumor_grade == other._tumor_grade \
            and self._pathological_stage == other._pathological_stage \
            and self._pathological_tnm_finding == other._pathological_tnm_finding \
            and self._diagnostic_markers == other._diagnostic_markers \
            and self._procedure == other._procedure \
            and self._files == other._files \
            and self._material_sample == other._material_sample \
            and self._sample_processing == other._sample_processing \
            and self._sample_storage == other._sample_storage

    def __repr__(self):
        return f'Biosample(' \
               f'id={self._id}, ' \
               f'individual_id={self._individual_id}, ' \
               f'derived_from_id={self._derived_from_id}, ' \
               f'description={self._description}, ' \
               f'sampled_tissue={self._sampled_tissue}, ' \
               f'sample_type={self._sample_type}, ' \
               f'phenotypic_features={self._phenotypic_features}, ' \
               f'measurements={self._measurements}, ' \
               f'taxonomy={self._taxonomy}, ' \
               f'time_of_collection={self._time_of_collection}, ' \
               f'histological_diagnosis={self._histological_diagnosis}, ' \
               f'tumor_progression={self._tumor_progression}, ' \
               f'tumor_grade={self._tumor_grade}, ' \
               f'pathological_stage={self._pathological_stage}, ' \
               f'pathological_tnm_finding={self._pathological_tnm_finding}, ' \
               f'diagnostic_markers={self._diagnostic_markers}, ' \
               f'procedure={self._procedure}, ' \
               f'files={self._files}, ' \
               f'material_sample={self._material_sample}, ' \
               f'sample_processing={self._sample_processing}, ' \
               f'sample_storage={self._sample_storage})'
