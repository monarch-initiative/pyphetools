import enum
import typing

from ._base import OntologyClass, TimeElement, ExternalReference, TimeInterval, Procedure
from ._measurement import Quantity


class TherapeuticRegimen:
    class RegimenStatus(enum.Enum):
        UNKNOWN_STATUS = 0
        STARTED = 1
        COMPLETED = 2
        DISCONTINUED = 3

    def __init__(
            self,
            identifier: typing.Union[OntologyClass, ExternalReference],
            status: RegimenStatus,
            start_time: typing.Optional[TimeElement] = None,
            end_time: typing.Optional[TimeElement] = None,
    ):
        self._identifier = identifier
        self._status = status
        self._start_time = start_time
        self._end_time = end_time


class RadiationTherapy:

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


class DrugType(enum.Enum):
    UNKNOWN_DRUG_TYPE = 0
    PRESCRIPTION = 1
    EHR_MEDICATION_LIST = 2
    ADMINISTRATION_RELATED_TO_PROCEDURE = 3


class DoseInterval:

    def __init__(
            self,
            quantity: Quantity,
            schedule_frequency: OntologyClass,
            interval: TimeInterval,
    ):
        self._quantity = quantity
        self._schedule_frequency = schedule_frequency
        self._interval = interval


class Treatment:

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
        self._dose_intervals = dose_intervals
        self._drug_type = drug_type
        self._cumulative_dose = cumulative_dose


class MedicalAction:

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
        self._adverse_events = adverse_events
        self._treatment_termination_reason = treatment_termination_reason
