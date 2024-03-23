import enum
import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import OntologyClass, TimeElement, ExternalReference, TimeInterval, Procedure
from ._measurement import Quantity

from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_oneof_scalar
from ..parse import extract_pb_message_scalar, extract_pb_message_seq, extract_pb_oneof_scalar


class TherapeuticRegimen(MessageMixin):
    _ONEOF_IDENTIFIER = {'external_reference': ExternalReference, 'ontology_class': OntologyClass}

    class RegimenStatus(enum.Enum):
        UNKNOWN_STATUS = 0
        STARTED = 1
        COMPLETED = 2
        DISCONTINUED = 3

    def __init__(
            self,
            identifier: typing.Union[ExternalReference, OntologyClass],
            regimen_status: RegimenStatus,
            start_time: typing.Optional[TimeElement] = None,
            end_time: typing.Optional[TimeElement] = None,
    ):
        self._identifier = identifier
        self._regimen_status = regimen_status
        self._start_time = start_time
        self._end_time = end_time

    @property
    def identifier(self) -> typing.Union[ExternalReference, OntologyClass]:
        return self._identifier

    @property
    def external_reference(self) -> typing.Optional[ExternalReference]:
        return self._identifier if isinstance(self._identifier, ExternalReference) else None

    @external_reference.setter
    def external_reference(self, value: ExternalReference):
        self._identifier = value

    @property
    def ontology_class(self) -> typing.Optional[OntologyClass]:
        return self._identifier if isinstance(self._identifier, OntologyClass) else None

    @ontology_class.setter
    def ontology_class(self, value: OntologyClass):
        self._identifier = value

    @property
    def regimen_status(self) -> RegimenStatus:
        return self._regimen_status

    @regimen_status.setter
    def regimen_status(self, value: RegimenStatus):
        self._regimen_status = value

    @property
    def start_time(self) -> typing.Optional[TimeElement]:
        return self._start_time

    @start_time.setter
    def start_time(self, value: TimeElement):
        self._start_time = value

    @start_time.deleter
    def start_time(self):
        self._start_time = None

    @property
    def end_time(self) -> typing.Optional[TimeElement]:
        return self._end_time

    @end_time.setter
    def end_time(self, value: TimeElement):
        self._end_time = value

    @end_time.deleter
    def end_time(self):
        self._end_time = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'external_reference', 'ontology_class', 'regimen_status', 'start_time', 'end_time'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if 'regimen_status' in values and any(field in values for field in cls._ONEOF_IDENTIFIER):
            return TherapeuticRegimen(
                identifier=extract_oneof_scalar(cls._ONEOF_IDENTIFIER, values),
                regimen_status=MessageMixin._extract_enum_field(
                    'regimen_status', TherapeuticRegimen.RegimenStatus, values,
                ),
                start_time=extract_message_scalar('start_time', TimeElement, values),
                end_time=extract_message_scalar('end_time', TimeElement, values),
            )
        else:
            raise ValueError(
                f'Missing one of required fields: `external_reference|ontology_class, regimen_status` {values}'
            )

    def to_message(self) -> Message:
        tr = pp202.TherapeuticRegimen(
            regimen_status=pp202.TherapeuticRegimen.RegimenStatus.Value(self._regimen_status.name),
        )

        if isinstance(self._identifier, ExternalReference):
            tr.external_reference.CopyFrom(self._identifier.to_message())
        elif isinstance(self._identifier, OntologyClass):
            tr.ontology_class.CopyFrom(self._identifier.to_message())
        else:
            raise ValueError('Bug')

        if self._start_time is not None:
            tr.start_time.CopyFrom(self._start_time.to_message())

        if self._end_time is not None:
            tr.end_time.CopyFrom(self._end_time.to_message())

        return tr

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.TherapeuticRegimen

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return TherapeuticRegimen(
                identifier=extract_pb_oneof_scalar('identifier', cls._ONEOF_IDENTIFIER, msg),
                regimen_status=TherapeuticRegimen.RegimenStatus(msg.regimen_status),
                start_time=extract_pb_message_scalar('start_time', TimeElement, msg),
                end_time=extract_pb_message_scalar('end_time', TimeElement, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, TherapeuticRegimen) \
            and self._identifier == other._identifier \
            and self._regimen_status == other._regimen_status \
            and self._start_time == other._start_time \
            and self._end_time == other._end_time

    def __repr__(self):
        return f'TherapeuticRegimen(identifier={self._identifier}, ' \
               f'regimen_status={self._regimen_status}, ' \
               f'start_time={self._start_time}, ' \
               f'end_time={self._end_time})'


class RadiationTherapy(MessageMixin):

    def __init__(
            self,
            modality: OntologyClass,
            body_site: OntologyClass,
            dosage: int,
            fractions: int,
    ):
        self._modality = modality
        self._body_site = body_site
        self._dosage = dosage
        self._fractions = fractions

    @property
    def modality(self) -> OntologyClass:
        return self._modality

    @modality.setter
    def modality(self, value: OntologyClass):
        self._modality = value

    @property
    def body_site(self) -> OntologyClass:
        return self._body_site

    @body_site.setter
    def body_site(self, value: OntologyClass):
        self._body_site = value

    @property
    def dosage(self) -> int:
        return self._dosage

    @dosage.setter
    def dosage(self, value: int):
        self._dosage = value

    @property
    def fractions(self) -> int:
        return self._fractions

    @fractions.setter
    def fractions(self, value: int):
        self._fractions = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'modality', 'body_site', 'dosage', 'fractions'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'modality', 'body_site', 'dosage', 'fractions'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return RadiationTherapy(
                modality=extract_message_scalar('modality', OntologyClass, values),
                body_site=extract_message_scalar('body_site', OntologyClass, values),
                dosage=values['dosage'],
                fractions=values['fractions'],
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.RadiationTherapy(
            modality=self._modality.to_message(),
            body_site=self._body_site.to_message(),
            dosage=self._dosage,
            fractions=self._fractions,
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.RadiationTherapy

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.RadiationTherapy):
            return RadiationTherapy(
                modality=extract_pb_message_scalar('modality', OntologyClass, msg),
                body_site=extract_pb_message_scalar('body_site', OntologyClass, msg),
                dosage=msg.dosage,
                fractions=msg.fractions,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, RadiationTherapy) \
            and self._modality == other._modality \
            and self._body_site == other._body_site \
            and self._dosage == other._dosage \
            and self._fractions == other._fractions

    def __repr__(self):
        return f'RadiationTherapy(modality={self._modality}, ' \
               f'body_site={self._modality}, ' \
               f'dosage={self._body_site}, ' \
               f'fractions={self._dosage})'


class DrugType(enum.Enum):
    UNKNOWN_DRUG_TYPE = 0
    PRESCRIPTION = 1
    EHR_MEDICATION_LIST = 2
    ADMINISTRATION_RELATED_TO_PROCEDURE = 3


class DoseInterval(MessageMixin):

    def __init__(
            self,
            quantity: Quantity,
            schedule_frequency: OntologyClass,
            interval: TimeInterval,
    ):
        self._quantity = quantity
        self._schedule_frequency = schedule_frequency
        self._interval = interval

    @property
    def quantity(self) -> Quantity:
        return self._quantity

    @quantity.setter
    def quantity(self, value: Quantity):
        self._quantity = value

    @property
    def schedule_frequency(self) -> OntologyClass:
        return self._schedule_frequency

    @schedule_frequency.setter
    def schedule_frequency(self, value: OntologyClass):
        self._schedule_frequency = value

    @property
    def interval(self) -> TimeInterval:
        return self._interval

    @interval.setter
    def interval(self, value: TimeInterval):
        self._interval = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'quantity', 'schedule_frequency', 'interval'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'quantity', 'schedule_frequency', 'interval'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return DoseInterval(
                quantity=extract_message_scalar('quantity', Quantity, values),
                schedule_frequency=extract_message_scalar('schedule_frequency', OntologyClass, values),
                interval=extract_message_scalar('interval', TimeInterval, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.DoseInterval(
            quantity=self._quantity.to_message(),
            schedule_frequency=self._schedule_frequency.to_message(),
            interval=self._interval.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.DoseInterval

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.DoseInterval):
            return DoseInterval(
                quantity=extract_pb_message_scalar('quantity', Quantity, msg),
                schedule_frequency=extract_pb_message_scalar('schedule_frequency', OntologyClass, msg),
                interval=extract_pb_message_scalar('interval', TimeInterval, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, DoseInterval) \
            and self._quantity == other._quantity \
            and self._schedule_frequency == other._schedule_frequency \
            and self._interval == other._interval

    def __repr__(self):
        return f'DoseInterval(quantity={self._quantity}, ' \
               f'schedule_frequency={self._schedule_frequency}, ' \
               f'interval={self._interval})'


class Treatment(MessageMixin):

    def __init__(
            self,
            agent: OntologyClass,
            route_of_administration: typing.Optional[OntologyClass] = None,
            dose_intervals: typing.Optional[typing.Iterable[DoseInterval]] = None,
            drug_type: typing.Optional[DrugType] = None,
            cumulative_dose: typing.Optional[Quantity] = None,
    ):
        self._agent = agent
        self._route_of_administration = route_of_administration
        self._dose_intervals = [] if dose_intervals is None else list(dose_intervals)
        self._drug_type = DrugType.UNKNOWN_DRUG_TYPE if drug_type is None else drug_type
        self._cumulative_dose = cumulative_dose

    @property
    def agent(self) -> OntologyClass:
        return self._agent

    @agent.setter
    def agent(self, value: OntologyClass):
        self._agent = value

    @property
    def route_of_administration(self) -> typing.Optional[OntologyClass]:
        return self._route_of_administration

    @route_of_administration.setter
    def route_of_administration(self, value: OntologyClass):
        self._route_of_administration = value

    @route_of_administration.deleter
    def route_of_administration(self):
        self._route_of_administration = None

    @property
    def dose_intervals(self) -> typing.MutableSequence[DoseInterval]:
        return self._dose_intervals

    @property
    def drug_type(self) -> typing.Optional[DrugType]:
        return self._drug_type

    @drug_type.setter
    def drug_type(self, value: DrugType):
        self._drug_type = value

    @drug_type.deleter
    def drug_type(self):
        self._drug_type = None

    @property
    def cumulative_dose(self) -> typing.Optional[Quantity]:
        return self._cumulative_dose

    @cumulative_dose.setter
    def cumulative_dose(self, value: Quantity):
        self._cumulative_dose = value

    @cumulative_dose.deleter
    def cumulative_dose(self):
        self._cumulative_dose = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'agent', 'route_of_administration', 'dose_intervals', 'drug_type', 'cumulative_dose'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'agent',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Treatment(
                agent=extract_message_scalar('agent', OntologyClass, values),
                route_of_administration=extract_message_scalar('route_of_administration', OntologyClass, values),
                dose_intervals=extract_message_sequence('dose_intervals', DoseInterval, values),
                drug_type=MessageMixin._extract_enum_field('drug_type', DrugType, values),
                cumulative_dose=extract_message_scalar('cumulative_dose', Quantity, values),
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Treatment

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Treatment):
            return Treatment(
                agent=extract_pb_message_scalar('agent', OntologyClass, msg),
                route_of_administration=extract_pb_message_scalar('route_of_administration', OntologyClass, msg),
                dose_intervals=extract_pb_message_seq('dose_intervals', DoseInterval, msg),
                drug_type=DrugType(msg.drug_type),
                cumulative_dose=extract_pb_message_scalar('cumulative_dose', Quantity, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def to_message(self) -> Message:
        t = pp202.Treatment(agent=self._agent.to_message(), )

        if self._route_of_administration is not None:
            t.route_of_administration.CopyFrom(self._route_of_administration.to_message())

        t.dose_intervals.extend(di.to_message() for di in self._dose_intervals)

        if self._drug_type is None:
            t.drug_type = pp202.DrugType.Value(DrugType.UNKNOWN_DRUG_TYPE.name)
        else:
            t.drug_type = pp202.DrugType.Value(self._drug_type.name)

        if self._cumulative_dose is not None:
            t.cumulative_dose.CopyFrom(self._cumulative_dose.to_message())

        return t

    def __eq__(self, other):
        return isinstance(other, Treatment) \
            and self._agent == other._agent \
            and self._route_of_administration == other._route_of_administration \
            and self._dose_intervals == other._dose_intervals \
            and self._drug_type == other._drug_type \
            and self._cumulative_dose == other._cumulative_dose

    def __repr__(self):
        return f'Treatment(agent={self._agent}, ' \
               f'route_of_administration={self._route_of_administration}, ' \
               f'dose_intervals={self._dose_intervals}, ' \
               f'drug_type={self._drug_type}, ' \
               f'cumulative_dose={self._cumulative_dose})'


class MedicalAction(MessageMixin):
    _CLS_ACTION = {
        'procedure': Procedure, 'treatment': Treatment,
        'radiation_therapy': RadiationTherapy,
        'therapeutic_regimen': TherapeuticRegimen,
    }

    def __init__(
            self,
            action: typing.Union[Procedure, Treatment, RadiationTherapy, TherapeuticRegimen],
            treatment_target: typing.Optional[OntologyClass] = None,
            treatment_intent: typing.Optional[OntologyClass] = None,
            response_to_treatment: typing.Optional[OntologyClass] = None,
            adverse_events: typing.Optional[typing.Iterable[OntologyClass]] = None,
            treatment_termination_reason: typing.Optional[OntologyClass] = None,
    ):
        self._action = action
        self._treatment_target = treatment_target
        self._treatment_intent = treatment_intent
        self._response_to_treatment = response_to_treatment
        self._adverse_events = [] if adverse_events is None else list(adverse_events)
        self._treatment_termination_reason = treatment_termination_reason

    @property
    def action(self) -> typing.Union[Procedure, Treatment, RadiationTherapy, TherapeuticRegimen]:
        return self._action

    @property
    def procedure(self) -> Procedure:
        return self._action if isinstance(self._action, Procedure) else None

    @procedure.setter
    def procedure(self, value: Procedure):
        self._action = value

    @property
    def treatment(self) -> Treatment:
        return self._action if isinstance(self._action, Treatment) else None

    @treatment.setter
    def treatment(self, value: Treatment):
        self._action = value

    @property
    def radiation_therapy(self) -> RadiationTherapy:
        return self._action if isinstance(self._action, RadiationTherapy) else None

    @radiation_therapy.setter
    def radiation_therapy(self, value: RadiationTherapy):
        self._action = value

    @property
    def therapeutic_regimen(self) -> TherapeuticRegimen:
        return self._action if isinstance(self._action, TherapeuticRegimen) else None

    @therapeutic_regimen.setter
    def therapeutic_regimen(self, value: TherapeuticRegimen):
        self._action = value

    @property
    def treatment_target(self) -> typing.Optional[OntologyClass]:
        return self._treatment_target

    @treatment_target.setter
    def treatment_target(self, value: OntologyClass):
        self._treatment_target = value

    @treatment_target.deleter
    def treatment_target(self):
        self._treatment_target = None

    @property
    def treatment_intent(self) -> typing.Optional[OntologyClass]:
        return self._treatment_intent

    @treatment_intent.setter
    def treatment_intent(self, value: OntologyClass):
        self._treatment_intent = value

    @treatment_intent.deleter
    def treatment_intent(self):
        self._treatment_intent = None

    @property
    def response_to_treatment(self) -> typing.Optional[OntologyClass]:
        return self._response_to_treatment

    @response_to_treatment.setter
    def response_to_treatment(self, value: OntologyClass):
        self._response_to_treatment = value

    @response_to_treatment.deleter
    def response_to_treatment(self):
        self._response_to_treatment = None

    @property
    def adverse_events(self) -> typing.MutableSequence[OntologyClass]:
        return self._adverse_events

    @property
    def treatment_termination_reason(self) -> typing.Optional[OntologyClass]:
        return self._treatment_termination_reason

    @treatment_termination_reason.setter
    def treatment_termination_reason(self, value: OntologyClass):
        self._treatment_termination_reason = value

    @treatment_termination_reason.deleter
    def treatment_termination_reason(self):
        self._treatment_termination_reason = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return (
            'procedure', 'treatment', 'radiation_therapy', 'therapeutic_regimen',
            'treatment_target', 'treatment_intent', 'response_to_treatment', 'adverse_events',
            'treatment_termination_reason',
        )

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        raise NotImplementedError('Should not be called!')

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if any(field in values for field in cls._CLS_ACTION):
            return MedicalAction(
                action=extract_oneof_scalar(cls._CLS_ACTION, values),
                treatment_target=extract_message_scalar('treatment_target', OntologyClass, values),
                treatment_intent=extract_message_scalar('treatment_intent', OntologyClass, values),
                response_to_treatment=extract_message_scalar('response_to_treatment', OntologyClass, values),
                adverse_events=extract_message_sequence('adverse_events', OntologyClass, values),
                treatment_termination_reason=extract_message_scalar(
                    'treatment_termination_reason', OntologyClass, values),
            )
        else:
            raise ValueError(
                f'Missing one of required fields: `procedure|treatment|radiation_therapy|therapeutic_regimen` {values}'
            )

    def to_message(self) -> Message:
        m = pp202.MedicalAction()

        if isinstance(self._action, Procedure):
            m.procedure.CopyFrom(self._action.to_message())
        elif isinstance(self._action, Treatment):
            m.treatment.CopyFrom(self._action.to_message())
        elif isinstance(self._action, RadiationTherapy):
            m.radiation_therapy.CopyFrom(self._action.to_message())
        elif isinstance(self._action, TherapeuticRegimen):
            m.therapeutic_regimen.CopyFrom(self._action.to_message())
        else:
            raise ValueError('Bug')

        if self._treatment_target is not None:
            m.treatment_target.CopyFrom(self._treatment_target.to_message())

        if self._treatment_intent is not None:
            m.treatment_intent.CopyFrom(self._treatment_intent.to_message())

        if self._response_to_treatment is not None:
            m.response_to_treatment.CopyFrom(self._response_to_treatment.to_message())

        m.adverse_events.extend(a.to_message() for a in self._adverse_events)

        if self._treatment_termination_reason is not None:
            m.treatment_termination_reason.CopyFrom(self._treatment_termination_reason.to_message())

        return m

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.MedicalAction

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return MedicalAction(
                action=extract_pb_oneof_scalar('action', cls._CLS_ACTION, msg),
                treatment_target=extract_pb_message_scalar('treatment_target', OntologyClass, msg),
                treatment_intent=extract_pb_message_scalar('treatment_intent', OntologyClass, msg),
                response_to_treatment=extract_pb_message_scalar('response_to_treatment', OntologyClass,
                                                                msg),
                adverse_events=extract_pb_message_seq('adverse_events', OntologyClass, msg),
                treatment_termination_reason=extract_pb_message_scalar(
                    'treatment_termination_reason', OntologyClass, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, MedicalAction) \
            and self._action == other._action \
            and self._treatment_target == other._treatment_target \
            and self._treatment_intent == other._treatment_intent \
            and self._response_to_treatment == other._response_to_treatment \
            and self._adverse_events == other._adverse_events \
            and self._treatment_termination_reason == other._treatment_termination_reason

    def __repr__(self):
        return f'MedicalAction(' \
               f'action={self._action}, ' \
               f'treatment_target={self._treatment_target}, ' \
               f'treatment_intent={self._treatment_intent}, ' \
               f'response_to_treatment={self._response_to_treatment}, ' \
               f'adverse_events={self._adverse_events}, ' \
               f'treatment_termination_reason={self._treatment_termination_reason})'
