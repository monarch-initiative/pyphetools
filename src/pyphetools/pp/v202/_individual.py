import enum
import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import TimeElement, OntologyClass
from .._api import MessageMixin
from .._timestamp import Timestamp
from ..parse import extract_message_scalar, extract_pb_message_scalar


class Sex(enum.Enum):
    """
    An enumeration used to represent the sex of an individual. This element does not represent gender identity
    or :class:`KaryotypicSex`, but instead represents typical “phenotypic sex”, as would be determined
    by a midwife or physician at birth.
    """
    # The `int` values correspond to protobuf fields in Phenopacket Schema.

    UNKNOWN_SEX = 0
    """
    Not assessed or not available. 
    Maps to `NCIT:C17998 <https://www.ebi.ac.uk/ols/ontologies/ncit/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FNCIT_C17998>`_
    """

    FEMALE = 1
    """
    Female sex. 
    Maps to `NCIT:C46113 <https://www.ebi.ac.uk/ols/ontologies/ncit/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FNCIT_C46113>`_.
    """

    MALE = 2
    """
    Male sex. 
    Maps to `NCIT:C46112 <https://www.ebi.ac.uk/ols/ontologies/ncit/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FNCIT_C46112>`_
    """

    OTHER_SEX = 3
    """
    It is not possible to accurately assess the applicability of `MALE`/`FEMALE`. 
    Maps to `NCIT:C45908 <https://www.ebi.ac.uk/ols/ontologies/ncit/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FNCIT_C45908>`_
    """


class KaryotypicSex(enum.Enum):

    # The `int` values correspond to protobuf fields in Phenopacket Schema.
    UNKNOWN_KARYOTYPE = 0
    XX = 1
    XY = 2
    XO = 3
    XXY = 4
    XXX = 5
    XXYY = 6
    XXXY = 7
    XXXX = 8
    XYY = 9
    OTHER_KARYOTYPE = 10


class VitalStatus(MessageMixin):
    """
    TODO: add docs.
    """

    class Status(enum.Enum):
        """
        TODO: add docs.
        """
        # The `int` values correspond to protobuf fields in Phenopacket Schema.

        UNKNOWN_STATUS = 0
        ALIVE = 1
        DECEASED = 2

    def __init__(
            self,
            status: Status,
            time_of_death: typing.Optional[TimeElement] = None,
            cause_of_death: typing.Optional[OntologyClass] = None,
            survival_time_in_days: typing.Optional[int] = None,
    ):
        self._status = status
        self._time_of_death = time_of_death
        self._cause_of_death = cause_of_death
        self._survival_time_in_days = survival_time_in_days

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, value: Status):
        self._status = value

    @property
    def time_of_death(self) -> typing.Optional[TimeElement]:
        return self._time_of_death

    @time_of_death.setter
    def time_of_death(self, value: typing.Optional[TimeElement]):
        self._time_of_death = value

    @time_of_death.deleter
    def time_of_death(self):
        self._time_of_death = None

    @property
    def cause_of_death(self) -> typing.Optional[OntologyClass]:
        return self._cause_of_death

    @cause_of_death.setter
    def cause_of_death(self, value: typing.Optional[OntologyClass]):
        self._cause_of_death = value

    @cause_of_death.deleter
    def cause_of_death(self):
        self._cause_of_death = None

    @property
    def survival_time_in_days(self) -> typing.Optional[int]:
        return self._survival_time_in_days

    @survival_time_in_days.setter
    def survival_time_in_days(self, value: typing.Optional[int]):
        self._survival_time_in_days = value

    @survival_time_in_days.deleter
    def survival_time_in_days(self):
        self._survival_time_in_days = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'status', 'time_of_death', 'cause_of_death', 'survival_time_in_days'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'status',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return VitalStatus(
                status=MessageMixin._extract_enum_field('status', VitalStatus.Status, values),
                time_of_death=extract_message_scalar('time_of_death', TimeElement, values),
                cause_of_death=extract_message_scalar('cause_of_death', OntologyClass, values),
                survival_time_in_days=int(values['survival_time_in_days']) if 'survival_time_in_days' in values else None,
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        vs = pp202.VitalStatus(
            status=pp202.VitalStatus.Status.Value(self._status.name),
        )

        if self._time_of_death is not None:
            vs.time_of_death.CopyFrom(self._time_of_death.to_message())


        if self._cause_of_death is not None:
            vs.cause_of_death.CopyFrom(self._cause_of_death.to_message())

        if self._survival_time_in_days is not None:
            vs.survival_time_in_days = self._survival_time_in_days

        return vs

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.VitalStatus

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.VitalStatus):
            return VitalStatus(
                status=VitalStatus.Status(msg.status),
                time_of_death=extract_pb_message_scalar('time_of_death', TimeElement, msg),
                cause_of_death=extract_pb_message_scalar('cause_of_death', OntologyClass, msg),
                survival_time_in_days=None if msg.survival_time_in_days == 0 else msg.survival_time_in_days,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, VitalStatus) \
            and self._status == other._status \
            and self._time_of_death == other._time_of_death \
            and self._cause_of_death == other._cause_of_death \
            and self._survival_time_in_days == other._survival_time_in_days

    def __repr__(self):
        return f'VitalStatus(' \
               f'status={self._status}, ' \
               f'time_of_death={self._time_of_death}, ' \
               f'cause_of_death={self._cause_of_death}, ' \
               f'survival_time_in_days={self._survival_time_in_days}' \
               ')'


class Individual(MessageMixin):

    def __init__(
            self,
            id: str,
            alternate_ids: typing.Optional[typing.Iterable[str]] = None,
            date_of_birth: typing.Optional[Timestamp] = None,
            time_at_last_encounter: typing.Optional[TimeElement] = None,
            vital_status: typing.Optional[VitalStatus] = None,
            sex: typing.Optional[Sex] = None,
            karyotypic_sex: typing.Optional[KaryotypicSex] = None,
            gender: typing.Optional[OntologyClass] = None,
            taxonomy: typing.Optional[OntologyClass] = None,
    ):
        # TODO: validate
        self._id = id
        self._alt_ids = [] if alternate_ids is None else list(alternate_ids)
        self._date_of_birth = date_of_birth
        self._time_at_last_encounter = time_at_last_encounter
        self._vital_status = vital_status
        self._sex = sex
        self._karyotypic_sex = karyotypic_sex
        self._gender = gender
        self._taxonomy = taxonomy

    @property
    def id(self) -> typing.Optional[str]:
        return self._id

    @property
    def alternate_ids(self) -> typing.MutableSequence[str]:
        return self._alt_ids

    @property
    def date_of_birth(self) -> typing.Optional[Timestamp]:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: typing.Optional[Timestamp]):
        self._date_of_birth = value

    @date_of_birth.deleter
    def date_of_birth(self):
        self._date_of_birth = None

    @property
    def time_at_last_encounter(self) -> typing.Optional[TimeElement]:
        return self._time_at_last_encounter

    @time_at_last_encounter.setter
    def time_at_last_encounter(self, value: typing.Optional[TimeElement]):
        self._time_at_last_encounter = value

    @time_at_last_encounter.deleter
    def time_at_last_encounter(self):
        self._time_at_last_encounter = None

    @property
    def vital_status(self) -> typing.Optional[VitalStatus]:
        return self._vital_status

    @vital_status.setter
    def vital_status(self, value: typing.Optional[VitalStatus]):
        self._vital_status = value

    @vital_status.deleter
    def vital_status(self):
        self._vital_status = None

    @property
    def sex(self) -> typing.Optional[Sex]:
        return self._sex

    @sex.setter
    def sex(self, value: typing.Optional[Sex]):
        self._sex = value

    @sex.deleter
    def sex(self):
        self._sex = None

    @property
    def karyotypic_sex(self) -> typing.Optional[KaryotypicSex]:
        return self._karyotypic_sex

    @karyotypic_sex.setter
    def karyotypic_sex(self, value: typing.Optional[KaryotypicSex]):
        self._karyotypic_sex = value

    @karyotypic_sex.deleter
    def karyotypic_sex(self):
        self._karyotypic_sex = None

    @property
    def gender(self) -> typing.Optional[OntologyClass]:
        return self._gender

    @gender.setter
    def gender(self, value: typing.Optional[OntologyClass]):
        self._gender = value

    @gender.deleter
    def gender(self):
        self._gender = None

    @property
    def taxonomy(self) -> typing.Optional[OntologyClass]:
        return self._taxonomy

    @taxonomy.setter
    def taxonomy(self, value: typing.Optional[OntologyClass]):
        self._taxonomy = value

    @taxonomy.deleter
    def taxonomy(self):
        self._taxonomy = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'alternate_ids', 'date_of_birth', 'time_at_last_encounter', 'vital_status', 'sex', 'karyotypic_sex', 'gender', 'taxonomy'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'id',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Individual(
                id=values['id'],
                alternate_ids=MessageMixin._extract_optional_field('alternate_ids', values),
                date_of_birth=extract_message_scalar('date_of_birth', Timestamp, values),
                time_at_last_encounter=extract_message_scalar('time_at_last_encounter', TimeElement, values),
                vital_status=extract_message_scalar('vital_status', VitalStatus, values),
                sex=MessageMixin._extract_enum_field('sex', Sex, values),
                karyotypic_sex=MessageMixin._extract_enum_field('karyotypic_sex', KaryotypicSex, values),
                gender=extract_message_scalar('gender', OntologyClass, values),
                taxonomy=extract_message_scalar('taxonomy', OntologyClass, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        i = pp202.Individual(
            id=self._id,
        )

        if len(self._alt_ids) != 0:
            i.alternate_ids.extend(self._alt_ids)

        if self._date_of_birth is not None:
            i.time_at_last_encounter.CopyFrom(self._date_of_birth.to_message())

        if self._time_at_last_encounter is not None:
            i.time_at_last_encounter.CopyFrom(self._time_at_last_encounter.to_message())

        if self._vital_status is not None:
            i.vital_status.CopyFrom(self._vital_status.to_message())

        if self._sex is not None:
            i.sex = pp202.Sex.Value(self._sex.name)

        if self._karyotypic_sex is not None:
            i.karyotypic_sex = pp202.KaryotypicSex.Value(self._karyotypic_sex.name)

        if self._gender is not None:
            i.gender.CopyFrom(self._gender.to_message())

        if self._taxonomy is not None:
            i.taxonomy.CopyFrom(self._taxonomy.to_message())

        return i

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Individual

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Individual):
            return Individual(
                id=msg.id,
                alternate_ids=msg.alternate_ids,
                date_of_birth=extract_pb_message_scalar('date_of_birth', Timestamp, msg),
                time_at_last_encounter=extract_pb_message_scalar('time_at_last_encounter', TimeElement, msg),
                sex=Sex(msg.sex),
                karyotypic_sex=KaryotypicSex(msg.karyotypic_sex),
                vital_status=extract_pb_message_scalar('vital_status', VitalStatus, msg),
                gender=extract_pb_message_scalar('gender', OntologyClass, msg),
                taxonomy=extract_pb_message_scalar('taxonomy', OntologyClass, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Individual) \
            and self._id == other._id \
            and self._alt_ids == other._alt_ids \
            and self._date_of_birth == other._date_of_birth \
            and self._time_at_last_encounter == other._time_at_last_encounter \
            and self._sex == other._sex \
            and self._karyotypic_sex == other._karyotypic_sex \
            and self._gender == other._gender \
            and self._taxonomy == other._taxonomy

    def __repr__(self):
        return f'Individual(id={self._id},' \
               f' alternate_ids={self._alt_ids},' \
               f' date_of_birth={self._date_of_birth},' \
               f' time_at_last_encounter={self._time_at_last_encounter},' \
               f' sex={self._sex},' \
               f' karyotypic_sex={self._karyotypic_sex},' \
               f' gender={self._gender},' \
               f' taxonomy={self._taxonomy},' \
               ')'
