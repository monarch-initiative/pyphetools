import typing

from .._api import MessageMixin, extract_message_mixin
from ._individual import Individual
from ._meta_data import MetaData


class Phenopacket(MessageMixin):

    def __init__(
            self,
            id: str,
            meta_data: MetaData,
            subject: typing.Optional[Individual] = None,
            # phenotypic_features: typing.Optional[typing.Iterable[]],
    ):
        self._id = id
        self._subject = subject
        self._meta_data = meta_data

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def subject(self) -> Individual:
        return self._subject

    @subject.setter
    def subject(self, value: Individual):
        self._subject = value

    @property
    def meta_data(self) -> MetaData:
        return self._meta_data

    @meta_data.setter
    def meta_data(self, value: MetaData):
        self._meta_data = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'subject', 'meta_data'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        return Phenopacket(
            id=values['id'],
            subject=extract_message_mixin('subject', Individual, values),
            # TODO: add the rest
            meta_data=MetaData.from_dict(values['meta_data']),
        )

    def __eq__(self, other):
        return isinstance(other, Phenopacket) \
            and self._id == other._id \
            and self._subject == other._subject \
            and self._meta_data == other._meta_data

    def __repr__(self):
        return f'Phenopacket(id={self._id}, subject={self._subject}, meta_data={self._meta_data})'
