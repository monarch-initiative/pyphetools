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
from ._phenotypic_feature import PhenotypicFeature
from ._disease import Disease
from ._meta_data import MetaData, Resource, Update
from ._phenopackets import Phenopacket
from ._vrsatile import Expression, Extension, VcfRecord, MoleculeContext, VariationDescriptor

__all__ = [
    'Phenopacket',
    'Individual', 'VitalStatus', 'Sex', 'KaryotypicSex',
    'GeneDescriptor', 'AcmgPathogenicityClassification', 'TherapeuticActionability', 'VariantInterpretation',
    'GenomicInterpretation', 'Diagnosis', 'Interpretation',
    'Expression', 'Extension', 'VcfRecord', 'MoleculeContext', 'VariationDescriptor',
    'PhenotypicFeature', 'Disease', 'Biosample',
    'MetaData', 'Resource', 'Update',
    'OntologyClass', 'ExternalReference', 'Evidence', 'Procedure', 'GestationalAge', 'Age', 'AgeRange', 'TimeInterval',
    'TimeElement', 'Timestamp', 'File',
]
