import typing

from ._base import File
from ._individual import Individual
from ._meta_data import MetaData
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence


class Phenopacket(MessageMixin):

    def __init__(
            self,
            id: str,
            meta_data: MetaData,
            # phenotypic_features: typing.Optional[typing.Iterable[]],
            subject: typing.Optional[Individual] = None,
            files: typing.Optional[typing.Iterable[File]] = None,
    ):
        self._id = id
        self._subject = subject
        self._files = None if files is None else list(files)
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
    def files(self) -> typing.Optional[typing.MutableSequence[File]]:
        return self._files

    @property
    def meta_data(self) -> MetaData:
        return self._meta_data

    @meta_data.setter
    def meta_data(self, value: MetaData):
        self._meta_data = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'subject', 'files', 'meta_data'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'id' in values:
            return Phenopacket(
                id=values['id'],
                subject=extract_message_scalar('subject', Individual, values),
                files=extract_message_sequence('files', File, values),
                # TODO: add the rest
                meta_data=MetaData.from_dict(values['meta_data']),
            )
        else:
            raise ValueError('Bug')  # TODO: better name

    def __eq__(self, other):
        return isinstance(other, Phenopacket) \
            and self._id == other._id \
            and self._subject == other._subject \
            and self._files == other._files \
            and self._meta_data == other._meta_data

    def __repr__(self):
        return f'Phenopacket(' \
               f'id={self._id}, ' \
               f'subject={self._subject}, ' \
               f'files={self._files}, ' \
               f'meta_data={self._meta_data})'
