"""
A package with types corresponding to the `v2.0.2` release of the Phenopacket Schema.
"""

# The private package members structure mimic the structure of the protobuf files of the `phenopacket-schema`.

from ._base import OntologyClass, ExternalReference, Evidence, Procedure
# We re-export Timestamp
from ._base import GestationalAge, Age, AgeRange, TimeInterval, TimeElement, Timestamp, File
from ._biosample import Biosample
from ._gene_descriptor import GeneDescriptor
from ._individual import Individual, KaryotypicSex, Sex, VitalStatus
from ._interpretation import AcmgPathogenicityClassification, TherapeuticActionability, VariantInterpretation
from ._interpretation import GenomicInterpretation, Diagnosis, Interpretation
from ._measurement import ReferenceRange, Quantity, TypedQuantity, ComplexValue, Value, Measurement
from ._medical_action import TherapeuticRegimen, RadiationTherapy, DrugType, DoseInterval, Treatment, MedicalAction
from ._phenotypic_feature import PhenotypicFeature
from ._disease import Disease
from ._meta_data import MetaData, Resource, Update
from ._phenopackets import Phenopacket
from ._vrs import Gene, Text, Number, IndefiniteRange, DefiniteRange, SimpleInterval, SequenceInterval
from ._vrs import SequenceLocation, SequenceState, LiteralSequenceExpression, DerivedSequenceExpression
from ._vrs import RepeatedSequenceExpression, CytobandInterval, ChromosomeLocation, Allele, Haplotype, CopyNumber
from ._vrs import VariationSet, Variation
from ._vrsatile import Expression, Extension, VcfRecord, MoleculeContext, VariationDescriptor

__all__ = [
    'Phenopacket',
    'Individual', 'VitalStatus', 'Sex', 'KaryotypicSex',
    'GeneDescriptor', 'AcmgPathogenicityClassification', 'TherapeuticActionability', 'VariantInterpretation',
    'GenomicInterpretation', 'Diagnosis', 'Interpretation',
    'ReferenceRange', 'Quantity', 'TypedQuantity', 'ComplexValue', 'Value', 'Measurement',
    'TherapeuticRegimen', 'RadiationTherapy', 'DrugType', 'DoseInterval', 'Treatment', 'MedicalAction',
    'Expression', 'Extension', 'VcfRecord', 'MoleculeContext', 'VariationDescriptor',
    'PhenotypicFeature', 'Disease', 'Biosample',
    'MetaData', 'Resource', 'Update',
    'OntologyClass', 'ExternalReference', 'Evidence', 'Procedure', 'GestationalAge', 'Age', 'AgeRange', 'TimeInterval',
    'TimeElement', 'Timestamp', 'File',
    # and the VRS members
    'Gene', 'Text', 'Number', 'IndefiniteRange', 'DefiniteRange', 'SimpleInterval', 'SequenceInterval',
    'SequenceLocation', 'SequenceState', 'LiteralSequenceExpression', 'DerivedSequenceExpression',
    'RepeatedSequenceExpression', 'CytobandInterval', 'ChromosomeLocation', 'Allele', 'Haplotype', 'CopyNumber',
    'VariationSet', 'Variation',
]
