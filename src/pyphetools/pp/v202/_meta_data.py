import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._base import ExternalReference
from .._api import MessageMixin
from .._timestamp import Timestamp
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class Resource(MessageMixin):

    def __init__(
            self,
            id: str,
            name: str,
            url: str,
            version: str,
            namespace_prefix: str,
            iri_prefix: str,
    ):
        self._id = id
        self._name = name
        self._url = url
        self._version = version
        self._namespace_prefix = namespace_prefix
        self._iri_prefix = iri_prefix

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value

    @property
    def namespace_prefix(self) -> str:
        return self._namespace_prefix

    @namespace_prefix.setter
    def namespace_prefix(self, value: str):
        self._namespace_prefix = value

    @property
    def iri_prefix(self) -> str:
        return self._iri_prefix

    @iri_prefix.setter
    def iri_prefix(self, value: str):
        self._iri_prefix = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'name', 'url', 'version', 'namespace_prefix', 'iri_prefix'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'id', 'name', 'url', 'version', 'namespace_prefix', 'iri_prefix'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Resource(
                id=values['id'],
                name=values['name'],
                url=values['url'],
                version=values['version'],
                namespace_prefix=values['namespace_prefix'],
                iri_prefix=values['iri_prefix'],
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Resource

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Resource(
                id=msg.id,
                name=msg.name,
                url=msg.url,
                version=msg.version,
                namespace_prefix=msg.namespace_prefix,
                iri_prefix=msg.iri_prefix,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def to_message(self) -> Message:
        return pp202.Resource(
            id=self._id,
            name=self._name,
            url=self._url,
            version=self._version,
            namespace_prefix=self._namespace_prefix,
            iri_prefix=self._iri_prefix,
        )

    def __eq__(self, other):
        return isinstance(other, Resource) \
            and self._id == other._id \
            and self._name == other._name \
            and self._url == other._url \
            and self._version == other._version \
            and self._namespace_prefix == other._namespace_prefix \
            and self._iri_prefix == other._iri_prefix

    def __repr__(self):
        return (f'Resource(id={self._id}, '
                f'name={self._name}, '
                f'url={self._url}, '
                f'version={self._version}, '
                f'namespace_prefix={self._namespace_prefix}, '
                f'iri_prefix={self._iri_prefix})')


class Update(MessageMixin):

    def __init__(
            self,
            timestamp: Timestamp,
            updated_by: typing.Optional[str] = None,
            comment: typing.Optional[str] = None,
    ):
        self._timestamp = timestamp
        self._updated_by = updated_by
        self._comment = comment

    @property
    def timestamp(self) -> Timestamp:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Timestamp):
        self._timestamp = value

    @property
    def updated_by(self) -> str:
        return self._updated_by

    @updated_by.setter
    def updated_by(self, value: str):
        self._updated_by = value

    @updated_by.deleter
    def updated_by(self):
        self._updated_by = None

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value

    @comment.deleter
    def comment(self):
        self._comment = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'timestamp', 'updated_by', 'comment'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'timestamp',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Update(
                timestamp=extract_message_scalar('timestamp', Timestamp, values),
                updated_by=values.get('updated_by', None),
                comment=values.get('comment', None),
            )
        else:
            cls._complain_about_missing_field(values)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Update

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Update(
                timestamp=extract_pb_message_scalar('timestamp', Timestamp, msg),
                updated_by=None if msg.updated_by == '' else msg.updated_by,
                comment=None if msg.comment == '' else msg.comment,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def to_message(self) -> Message:
        update = pp202.Update(timestamp=self._timestamp.to_message(), )

        if self._updated_by is not None:
            update.updated_by = self._updated_by

        if self._comment is not None:
            update.comment = self._comment

        return update

    def __eq__(self, other):
        return isinstance(other, Update) \
            and self._timestamp == other._timestamp \
            and self._updated_by == other._updated_by \
            and self._comment == other._comment

    def __repr__(self):
        return f'Update(timestamp={self._timestamp}, updated_by={self._updated_by}, comment={self._comment})'


class MetaData(MessageMixin):
    # TODO: this entire class must be implemented!

    def __init__(
            self,
            created: Timestamp,
            created_by: str,
            submitted_by: typing.Optional[str] = None,
            resources: typing.Optional[typing.Iterable[Resource]] = None,
            updates: typing.Optional[typing.Iterable[Update]] = None,
            phenopacket_schema_version: str = '2.0.2',
            external_references: typing.Optional[typing.Iterable[ExternalReference]] = None,
    ):
        self._created = created
        self._created_by = created_by
        self._submitted_by = submitted_by
        self._resources = [] if resources is None else list(resources)
        self._updates = [] if updates is None else list(updates)
        self._phenopacket_schema_version = phenopacket_schema_version
        self._external_references = [] if external_references is None else list(external_references)

    @property
    def created(self) -> Timestamp:
        return self._created

    @created.setter
    def created(self, value: Timestamp):
        self._created = value

    @property
    def created_by(self) -> str:
        return self._created_by

    @created_by.setter
    def created_by(self, value: str):
        self._created_by = value

    @property
    def submitted_by(self) -> typing.Optional[str]:
        return self._submitted_by

    @submitted_by.setter
    def submitted_by(self, value: typing.Optional[str]):
        self._submitted_by = value

    @submitted_by.deleter
    def submitted_by(self):
        self._submitted_by = None

    @property
    def resources(self) -> typing.MutableSequence[Resource]:
        return self._resources

    @property
    def updates(self) -> typing.MutableSequence[Update]:
        return self._updates

    @property
    def phenopacket_schema_version(self) -> str:
        return self._phenopacket_schema_version

    @phenopacket_schema_version.setter
    def phenopacket_schema_version(self, value: str):
        self._phenopacket_schema_version = value

    @property
    def external_references(self) -> typing.MutableSequence[ExternalReference]:
        return self._external_references

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'created', 'created_by', 'submitted_by', 'resources', 'updates', 'phenopacket_schema_version', 'external_references'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'created', 'created_by', 'phenopacket_schema_version',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return MetaData(
                created=Timestamp.from_str(values['created']),
                created_by=values['created_by'],
                submitted_by=values.get('submitted_by', None),
                resources=extract_message_sequence('resources', Resource, values),
                updates=extract_message_sequence('updates', Update, values),
                phenopacket_schema_version=values['phenopacket_schema_version'],
                external_references=extract_message_sequence('external_references', ExternalReference, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        meta_data = pp202.MetaData(
            created=self._created.to_message(),
            created_by=self._created_by,
            phenopacket_schema_version=self._phenopacket_schema_version,
        )

        if self._submitted_by is not None:
            meta_data.submitted_by = self._submitted_by

        meta_data.resources.extend(r.to_message() for r in self._resources)
        meta_data.resources.extend(u.to_message() for u in self._updates)
        meta_data.external_references.extend(er.to_message() for er in self._external_references)

        return meta_data

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.MetaData

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.MetaData):
            return MetaData(
                created=extract_pb_message_scalar('created', Timestamp, msg),
                created_by=msg.created_by,
                submitted_by=None if msg.submitted_by == '' else msg.submitted_by,
                resources=extract_pb_message_seq('resources', Resource, msg),
                updates=extract_pb_message_seq('updates', Update, msg),
                phenopacket_schema_version=msg.phenopacket_schema_version,
                external_references=extract_pb_message_seq('external_references', ExternalReference, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, MetaData) \
            and self._created == other._created \
            and self._created_by == other._created_by \
            and self._submitted_by == other._submitted_by \
            and self._resources == other._resources \
            and self._updates == other._updates \
            and self._phenopacket_schema_version == other._phenopacket_schema_version \
            and self._external_references == other._external_references

    def __repr__(self):
        return (f'MetaData('
                f'created={self._created}, '
                f'created_by={self._created_by}, '
                f'submitted_by={self._submitted_by}, '
                f'resources={self._resources}, '
                f'updates={self._updates}, '
                f'phenopacket_schema_version={self._phenopacket_schema_version}, '
                f'external_references={self._external_references})')
