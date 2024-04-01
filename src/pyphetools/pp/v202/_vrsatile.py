import enum
import typing

import phenopackets as pp202
from google.protobuf.message import Message

from ._gene_descriptor import GeneDescriptor
from ._base import OntologyClass
from ._vrs import Variation

from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class Expression(MessageMixin):

    def __init__(
            self,
            syntax: str,
            value: str,
            version: typing.Optional[str] = None,
    ):
        self._syntax = syntax
        self._value = value
        self._version = version

    @property
    def syntax(self) -> str:
        return self._syntax

    @syntax.setter
    def syntax(self, value: str):
        self._syntax = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    @property
    def version(self) -> typing.Optional[str]:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value

    @version.deleter
    def version(self):
        self._version = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'syntax', 'value', 'version'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'syntax', 'value',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Expression(
                syntax=values['syntax'],
                value=values['value'],
                version=values.get('version', None),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        expression = pp202.Expression(syntax=self._syntax, value=self._value)

        if self._version is not None:
            expression.version = self._version

        return expression

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Expression

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Expression(
                syntax=msg.syntax,
                value=msg.value,
                version=None if msg.version == '' else msg.version,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Expression) \
            and self._syntax == other._syntax \
            and self._value == other._value \
            and self._version == other._version

    def __repr__(self):
        return 'Expression(' \
               f'syntax={self._syntax}, ' \
               f'value={self._value}, ' \
               f'version={self._version})'


class Extension(MessageMixin):

    def __init__(
            self,
            name: str,
            value: str,
    ):
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'name', 'value'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'name', 'value'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return Extension(name=values['name'], value=values['value'])
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        return pp202.Extension(name=self._name, value=self._value)

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Extension

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return Extension(
                name=msg.name,
                value=msg.value,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Extension) and self._name == other._name and self._value == other._value

    def __repr__(self):
        return f'Extension(name={self._name}, value={self._value})'


class VcfRecord(MessageMixin):

    def __init__(
            self,
            genome_assembly: str,
            chrom: str,
            pos: int,
            ref: str,
            alt: str,
            id: typing.Optional[str] = None,
            qual: typing.Optional[str] = None,
            filter: typing.Optional[str] = None,
            info: typing.Optional[str] = None,
    ):
        self._genome_assembly = genome_assembly
        self._chrom = chrom
        self._pos = pos
        self._ref = ref
        self._alt = alt
        self._id = id
        self._qual = qual
        self._filter = filter
        self._info = info

    @property
    def genome_assembly(self) -> str:
        return self._genome_assembly

    @genome_assembly.setter
    def genome_assembly(self, value: str):
        self._genome_assembly = value

    @property
    def chrom(self) -> str:
        return self._chrom

    @chrom.setter
    def chrom(self, value: str):
        self._chrom = value

    @property
    def pos(self) -> int:
        return self._pos

    @pos.setter
    def pos(self, value: int):
        self._pos = value

    @property
    def ref(self) -> str:
        return self._ref

    @ref.setter
    def ref(self, value: str):
        self._ref = value

    @property
    def alt(self) -> str:
        return self._alt

    @alt.setter
    def alt(self, value: str):
        self._alt = value

    @property
    def id(self) -> typing.Optional[str]:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @id.deleter
    def id(self):
        self._id = None

    @property
    def qual(self) -> typing.Optional[str]:
        return self._qual

    @qual.setter
    def qual(self, value: str):
        self._qual = value

    @qual.deleter
    def qual(self):
        self._qual = None

    @property
    def filter(self) -> typing.Optional[str]:
        return self._filter

    @filter.setter
    def filter(self, value: str):
        self._filter = value

    @filter.deleter
    def filter(self):
        self._filter = None

    @property
    def info(self) -> typing.Optional[str]:
        return self._info

    @info.setter
    def info(self, value: str):
        self._info = value

    @info.deleter
    def info(self):
        self._info = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'genome_assembly', 'chrom', 'pos', 'ref', 'alt', 'id', 'qual', 'filter', 'info'

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'genome_assembly', 'chrom', 'pos', 'ref', 'alt'

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return VcfRecord(
                genome_assembly=values['genome_assembly'],
                chrom=values['chrom'],
                pos=values['pos'],
                ref=values['ref'],
                alt=values['alt'],
                id=MessageMixin._extract_optional_field('id', values),
                qual=MessageMixin._extract_optional_field('qual', values),
                filter=MessageMixin._extract_optional_field('filter', values),
                info=MessageMixin._extract_optional_field('info', values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        vcf = pp202.VcfRecord(
            genome_assembly=self._genome_assembly,
            chrom=self._chrom,
            pos=self._pos,
            ref=self._ref,
            alt=self._alt,
        )

        if self._id is not None:
            vcf.id = self._id

        if self._qual is not None:
            vcf.qual = self._qual

        if self._filter is not None:
            vcf.filter = self._filter

        if self._info is not None:
            vcf.info = self._info

        return vcf

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.VcfRecord

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return VcfRecord(
                genome_assembly=msg.genome_assembly,
                chrom=msg.chrom,
                pos=msg.pos,
                ref=msg.ref,
                alt=msg.alt,
                id=None if msg.id == '' else msg.id,
                qual=None if msg.qual == '' else msg.qual,
                filter=None if msg.filter == '' else msg.filter,
                info=None if msg.info == '' else msg.info,
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, VcfRecord) \
            and self._genome_assembly == other._genome_assembly \
            and self._chrom == other._chrom \
            and self._pos == other._pos \
            and self._ref == other._ref \
            and self._alt == other._alt \
            and self._id == other._id \
            and self._qual == other._qual \
            and self._filter == other._filter \
            and self._info == other._info

    def __repr__(self):
        return f'VcfRecord(genome_assembly={self._genome_assembly}, ' \
               f'chrom={self._chrom}, ' \
               f'pos={self._pos}, ' \
               f'ref={self._ref}, ' \
               f'alt={self._alt}, ' \
               f'id={self._id}, ' \
               f'qual={self._qual}, ' \
               f'filter={self._filter}, ' \
               f'info={self._info})'


class MoleculeContext(enum.Enum):
    unspecified_molecule_context = 0
    genomic = 1
    transcript = 2
    protein = 3


class VariationDescriptor(MessageMixin):

    def __init__(
            self,
            id: str,
            molecule_context: MoleculeContext,
            # variation: typing.Optional[Variation] = None,
            label: typing.Optional[str] = None,
            description: typing.Optional[str] = None,
            gene_context: typing.Optional[GeneDescriptor] = None,
            expressions: typing.Optional[typing.Iterable[Expression]] = None,
            vcf_record: typing.Optional[VcfRecord] = None,
            xrefs: typing.Optional[typing.Iterable[str]] = None,
            alternate_labels: typing.Optional[typing.Iterable[str]] = None,
            extensions: typing.Optional[typing.Iterable[Extension]] = None,
            structural_type: typing.Optional[OntologyClass] = None,
            vrs_ref_allele_seq: typing.Optional[str] = None,
            allelic_state: typing.Optional[OntologyClass] = None,
    ):
        self._id = id
        self._molecule_context = molecule_context
        # self._variation = variation
        self._label = label
        self._description = description
        self._gene_context = gene_context
        self._expressions = [] if expressions is None else list(expressions)
        self._vcf_record = vcf_record
        self._xrefs = [] if xrefs is None else list(xrefs)
        self._alternate_labels = [] if alternate_labels is None else list(alternate_labels)
        self._extensions = [] if extensions is None else list(extensions)
        self._structural_type = structural_type
        self._vrs_ref_allele_seq = vrs_ref_allele_seq
        self._allelic_state = allelic_state

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def molecule_context(self) -> MoleculeContext:
        return self._molecule_context

    @molecule_context.setter
    def molecule_context(self, value: MoleculeContext):
        self._molecule_context = value

    # @property
    # def variation(self) -> typing.Optional[Variation]:
    #     return self._variation
    #
    # @variation.setter
    # def variation(self, value: Variation):
    #     self._variation = value
    #
    # @variation.deleter
    # def variation(self):
    #     self._variation = None

    @property
    def label(self) -> typing.Optional[str]:
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @label.deleter
    def label(self):
        self._label = None

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
    def gene_context(self) -> typing.Optional[GeneDescriptor]:
        return self._gene_context

    @gene_context.setter
    def gene_context(self, value: GeneDescriptor):
        self._gene_context = value

    @gene_context.deleter
    def gene_context(self):
        self._gene_context = None

    @property
    def expressions(self) -> typing.MutableSequence[Expression]:
        return self._expressions

    @property
    def vcf_record(self) -> typing.Optional[VcfRecord]:
        return self._vcf_record

    @vcf_record.setter
    def vcf_record(self, value: VcfRecord):
        self._vcf_record = value

    @vcf_record.deleter
    def vcf_record(self):
        self._vcf_record = None

    @property
    def xrefs(self) -> typing.MutableSequence[str]:
        return self._xrefs

    @property
    def alternate_labels(self) -> typing.MutableSequence[str]:
        return self._alternate_labels

    @property
    def extensions(self) -> typing.MutableSequence[Extension]:
        return self._extensions

    @property
    def structural_type(self) -> typing.Optional[OntologyClass]:
        return self._structural_type

    @structural_type.setter
    def structural_type(self, value: OntologyClass):
        self._structural_type = value

    @structural_type.deleter
    def structural_type(self):
        self._structural_type = None

    @property
    def vrs_ref_allele_seq(self) -> typing.Optional[str]:
        return self._vrs_ref_allele_seq

    @vrs_ref_allele_seq.setter
    def vrs_ref_allele_seq(self, value: str):
        self._vrs_ref_allele_seq = value

    @vrs_ref_allele_seq.deleter
    def vrs_ref_allele_seq(self):
        self._vrs_ref_allele_seq = None

    @property
    def allelic_state(self) -> typing.Optional[OntologyClass]:
        return self._allelic_state

    @allelic_state.setter
    def allelic_state(self, value: OntologyClass):
        self._allelic_state = value

    @allelic_state.deleter
    def allelic_state(self):
        self._allelic_state = None

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return (
            'id', 'molecule_context',  # 'variation',
            'label', 'description', 'gene_context', 'expressions', 'vcf_record',
            'xrefs', 'alternate_labels', 'extensions', 'structural_type', 'vrs_ref_allele_seq', 'allelic_state',
        )

    @classmethod
    def required_fields(cls) -> typing.Sequence[str]:
        return 'id', 'molecule_context',

    @classmethod
    def from_dict(cls, values: typing.Mapping[str, typing.Any]):
        if cls._all_required_fields_are_present(values):
            return VariationDescriptor(
                id=values['id'],
                molecule_context=MessageMixin._extract_enum_field('molecule_context', MoleculeContext, values),
                # variation=extract_message_scalar('variation', Variation, values),
                label=values.get('label', None),
                description=values.get('description', None),
                gene_context=extract_message_scalar('gene_context', GeneDescriptor, values),
                expressions=extract_message_sequence('expressions', Expression, values),
                vcf_record=extract_message_scalar('vcf_record', VcfRecord, values),
                xrefs=values.get('xrefs', None),
                alternate_labels=values.get('alternate_labels', None),
                extensions=extract_message_sequence('extensions', Extension, values),
                structural_type=extract_message_scalar('structural_type', OntologyClass, values),
                vrs_ref_allele_seq=values.get('vrs_ref_allele_seq', None),
                allelic_state=extract_message_scalar('allelic_state', OntologyClass, values),
            )
        else:
            cls._complain_about_missing_field(values)

    def to_message(self) -> Message:
        vd = pp202.VariationDescriptor(
            id=self._id,
            molecule_context=pp202.MoleculeContext.Value(self._molecule_context.name),
        )

        # if self._variation is not None:
        #     vd.variation.CopyFrom(self._variation.to_message())

        if self._label is not None:
            vd.label = self._label

        if self._description is not None:
            vd.description = self._description

        if self._gene_context is not None:
            vd.gene_context.CopyFrom(self._gene_context.to_message())

        vd.expressions.extend(e.to_message() for e in self._expressions)

        if self._vcf_record is not None:
            vd.vcf_record.CopyFrom(self._vcf_record.to_message())

        vd.xrefs.extend(self._xrefs)
        vd.alternate_labels.extend(self._alternate_labels)
        vd.extensions.extend(e.to_message() for e in self._extensions)

        if self._structural_type is not None:
            vd.structural_type.CopyFrom(self._structural_type.to_message())

        if self._vrs_ref_allele_seq is not None:
            self.vrs_ref_allele_seq = self._vrs_ref_allele_seq

        if self._allelic_state is not None:
            vd.allelic_state.CopyFrom(self._allelic_state.to_message())

        return vd

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.VariationDescriptor

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, cls.message_type()):
            return VariationDescriptor(
                id=msg.id,
                molecule_context=MoleculeContext(msg.molecule_context),
                # variation=extract_pb_message_scalar('variation', Variation, msg),
                label=None if msg.label == '' else msg.label,
                description=None if msg.description == '' else msg.description,
                gene_context=extract_pb_message_scalar('gene_context', GeneDescriptor, msg),
                expressions=extract_pb_message_seq('expressions', Expression, msg),
                vcf_record=extract_pb_message_scalar('vcf_record', VcfRecord, msg),
                xrefs=msg.xrefs,
                alternate_labels=msg.alternate_labels,
                extensions=extract_pb_message_seq('extensions', Extension, msg),
                structural_type=extract_pb_message_scalar('structural_type', OntologyClass, msg),
                vrs_ref_allele_seq=None if msg.vrs_ref_allele_seq == '' else msg.vrs_ref_allele_seq,
                allelic_state=extract_pb_message_scalar('allelic_state', OntologyClass, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        # and self._variation == other._variation \
        return isinstance(other, VariationDescriptor) \
            and self._id == other._id \
            and self._molecule_context == other._molecule_context \
            and self._label == other._label \
            and self._description == other._description \
            and self._gene_context == other._gene_context \
            and self._expressions == other._expressions \
            and self._vcf_record == other._vcf_record \
            and self._xrefs == other._xrefs \
            and self._alternate_labels == other._alternate_labels \
            and self._extensions == other._extensions \
            and self._structural_type == other._structural_type \
            and self._vrs_ref_allele_seq == other._vrs_ref_allele_seq \
            and self._allelic_state == other._allelic_state

    def __repr__(self):
        # f'variation={self._variation}, ' \
        return 'VariationDescriptor(' \
               f'id={self._id}, ' \
               f'molecule_context={self._molecule_context}, ' \
               f'label={self._label}, ' \
               f'description={self._description}, ' \
               f'gene_context={self._gene_context}, ' \
               f'expressions={self._expressions}, ' \
               f'vcf_record={self._vcf_record}, ' \
               f'xrefs={self._xrefs}, ' \
               f'alternate_labels={self._alternate_labels}, ' \
               f'extensions={self._extensions}, ' \
               f'structural_type={self._structural_type}, ' \
               f'vrs_ref_allele_seq={self._vrs_ref_allele_seq}, ' \
               f'allelic_state={self._allelic_state})'
