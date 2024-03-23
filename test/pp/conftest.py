import typing

import pytest

from pyphetools.pp.v202 import *


@pytest.fixture(scope='package')
def retinoblastoma(
        individual: Individual,
        phenotypic_features: typing.Sequence[PhenotypicFeature],
        measurements: typing.Sequence[Measurement],
        biosamples: typing.Sequence[Biosample],
        interpretations: typing.Sequence[Interpretation],
        diseases: typing.Sequence[Disease],
        medical_actions: typing.Sequence[MedicalAction],
        files: typing.Sequence[File],
        meta_data: MetaData,
) -> Phenopacket:
    """
    Phenopacket with the same values that we can find in `test/data/pp/retinoblastoma.json`.
    """
    return Phenopacket(
        id='example.retinoblastoma.phenopacket.id',
        subject=individual,
        phenotypic_features=phenotypic_features,
        measurements=measurements,
        biosamples=biosamples,
        interpretations=interpretations,
        diseases=diseases,
        medical_actions=medical_actions,
        files=files,
        meta_data=meta_data,
    )


@pytest.fixture(scope='package')
def individual() -> Individual:
    """
    `Individual` from the `retinoblastoma` phenopacket.
    """
    return Individual(
        id='proband A',
        alternate_ids=('some', 'other', 'identifiers'),
        time_at_last_encounter=TimeElement(
            element=Age(
                iso8601duration='P6M',
            )
        ),
        vital_status=VitalStatus(
            status=VitalStatus.Status.DECEASED,
            time_of_death=TimeElement(element=Age(iso8601duration='P1Y')),
            cause_of_death=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            survival_time_in_days=180,
        ),
        sex=Sex.FEMALE,
        karyotypic_sex=KaryotypicSex.XX,
        taxonomy=OntologyClass(id='NCBITaxon:9606', label='Homo sapiens')
    )


@pytest.fixture(scope='package')
def phenotypic_features() -> typing.Sequence[PhenotypicFeature]:
    return (
        PhenotypicFeature(
            type=OntologyClass(id='HP:0030084', label='Clinodactyly'),
            modifiers=(OntologyClass(id='HP:0012834', label='Right'),),
            onset=TimeElement(element=Age(iso8601duration='P3M')),
        ),
        PhenotypicFeature(
            type=OntologyClass(id='HP:0000555', label='Leukocoria'),
            modifiers=(OntologyClass(id='HP:0012835', label='Left'),),
            onset=TimeElement(element=Age(iso8601duration='P4M')),
        ),
        PhenotypicFeature(
            type=OntologyClass(id='HP:0000486', label='Strabismus'),
            modifiers=(OntologyClass(id='HP:0012835', label='Left'),),
            onset=TimeElement(element=Age(iso8601duration='P5M15D')),
        ),
        PhenotypicFeature(
            type=OntologyClass(id='HP:0000541', label='Retinal detachment'),
            modifiers=(OntologyClass(id='HP:0012835', label='Left'),),
            onset=TimeElement(element=Age(iso8601duration='P6M')),
        ),
    )


@pytest.fixture(scope='package')
def measurements() -> typing.Sequence[Measurement]:
    return (
        Measurement(
            assay=OntologyClass(id='LOINC:79893-4', label='Left eye Intraocular pressure'),
            measurement_value=Value(
                value=Quantity(
                    unit=OntologyClass(id='UCUM:mm[Hg]', label='millimetres of mercury'),
                    value=25.0,
                    reference_range=ReferenceRange(
                        unit=OntologyClass(id='LOINC:56844-4', label='Intraocular pressure of Eye'),
                        low=10.0,
                        high=21.0,
                    ),
                ),
            ),
            time_observed=TimeElement(
                element=Age(iso8601duration='P6M'),
            ),
        ),
        Measurement(
            assay=OntologyClass(id='LOINC:79892-6', label='Right eye Intraocular pressure'),
            measurement_value=Value(
                value=Quantity(
                    unit=OntologyClass(id='UCUM:mm[Hg]', label='millimetres of mercury'),
                    value=15.0,
                    reference_range=ReferenceRange(
                        unit=OntologyClass(id='LOINC:56844-4', label='Intraocular pressure of Eye'),
                        low=10.0,
                        high=21.0,
                    ),
                ),
            ),
            time_observed=TimeElement(
                element=Age(iso8601duration='P6M'),
            ),
        ),
    )


@pytest.fixture(scope='package')
def diseases() -> typing.Sequence[Disease]:
    return (
        Disease(
            term=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            onset=TimeElement(element=Age(iso8601duration='P4M')),
            disease_stage=(OntologyClass(id='LOINC:LA24739-7', label='Group E'),),
            clinical_tnm_finding=(OntologyClass(id='NCIT:C140678', label='Retinoblastoma cM0 TNM Finding v8'),),
            primary_site=OntologyClass(id='UBERON:0004548', label='left eye'),
        ),
    )


@pytest.fixture(scope='package')
def interpretations() -> typing.Sequence[Interpretation]:
    return (
        Interpretation(
            id='interpretation.id',
            progress_status=Interpretation.ProgressStatus.SOLVED,
            diagnosis=Diagnosis(
                disease=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
                genomic_interpretations=(
                    GenomicInterpretation(
                        subject_or_biosample_id='proband A',
                        interpretation_status=GenomicInterpretation.InterpretationStatus.CAUSATIVE,
                        variant_interpretation=VariantInterpretation(
                            acmg_pathogenicity_classification=AcmgPathogenicityClassification.PATHOGENIC,
                            therapeutic_actionability=TherapeuticActionability.ACTIONABLE,
                            variation_descriptor=VariationDescriptor(
                                id='example-cnv',
                                molecule_context=MoleculeContext.genomic,
                                # TODO: variation
                                extensions=(
                                    Extension(name='mosaicism', value='40.0%'),
                                ),
                            )
                        )
                    ),
                    GenomicInterpretation(
                        subject_or_biosample_id='biosample.1',
                        interpretation_status=GenomicInterpretation.InterpretationStatus.CAUSATIVE,
                        variant_interpretation=VariantInterpretation(
                            acmg_pathogenicity_classification=AcmgPathogenicityClassification.PATHOGENIC,
                            therapeutic_actionability=TherapeuticActionability.ACTIONABLE,
                            variation_descriptor=VariationDescriptor(
                                id='rs121913300',
                                molecule_context=MoleculeContext.genomic,
                                # TODO: variation
                                label='RB1 c.958C>T (p.Arg320Ter)',
                                gene_context=GeneDescriptor(value_id='HGNC:9884', symbol='RB1'),
                                expressions=(
                                    Expression(syntax='hgvs.c', value='NM_000321.2:c.958C>T'),
                                    Expression(syntax='transcript_reference', value='NM_000321.2'),
                                ),
                                vcf_record=VcfRecord(
                                    genome_assembly="GRCh38",
                                    chrom="NC_000013.11",
                                    pos=48367512,
                                    ref="C",
                                    alt="T",
                                ),
                                extensions=(
                                    Extension(name='allele-frequency', value='25.0%'),
                                ),
                                allelic_state=OntologyClass(id='GENO:0000135', label='heterozygous'),
                            )
                        )
                    )
                ),
            ),
        ),
    )


@pytest.fixture(scope='package')
def biosamples() -> typing.Sequence[Biosample]:
    return (
        Biosample(
            id='biosample.1',
            sampled_tissue=OntologyClass(id='UBERON:0000970', label='eye'),
            phenotypic_features=(
                PhenotypicFeature(type=OntologyClass(id='NCIT:C35941', label='Flexner-Wintersteiner Rosette Formation')),
                PhenotypicFeature(type=OntologyClass(id='NCIT:C132485', label='Apoptosis and Necrosis')),
            ),
            measurements=(
                Measurement(
                    assay=OntologyClass(id='LOINC:33728-7', label='Size.maximum dimension in Tumor'),
                    measurement_value=Value(
                        value=Quantity(
                            unit=OntologyClass(id='UCUM:mm', label='millimeter'),
                            value=15.0,
                        )
                    ),
                    time_observed=TimeElement(
                        element=Age(iso8601duration='P8M2W')
                    )
                ),
            ),
            tumor_progression=OntologyClass(id='NCIT:C8509', label='Primary Neoplasm'),
            pathological_tnm_finding=(
                OntologyClass(id='NCIT:C140720', label='Retinoblastoma pT3 TNM Finding v8'),
                OntologyClass(id='NCIT:C140711', label='Retinoblastoma pN0 TNM Finding v8'),
            ),
            procedure=Procedure(
                code=OntologyClass(id='NCIT:C48601', label='Enucleation'),
                body_site=OntologyClass(id='UBERON:0004548', label='left eye'),
                performed=TimeElement(element=Age(iso8601duration='P8M2W'))
            ),
            files=(
                File(
                    uri='file://data/fileSomaticWgs.vcf.gz',
                    individual_to_file_identifiers={
                        'biosample.1': 'specimen.1',
                    },
                    file_attributes={
                        'fileFormat': 'VCF',
                        'genomeAssembly': 'GRCh38',
                    },
                ),
            ),
        ),
    )


@pytest.fixture(scope='package')
def medical_actions() -> typing.Sequence[MedicalAction]:
    return (
        MedicalAction(
            action=Treatment(
                agent=OntologyClass(id='DrugCentral:1678', label='melphalan'),
                route_of_administration=OntologyClass(id='NCIT:C38222', label='Intraarterial Route of Administration'),
                dose_intervals=(
                    DoseInterval(
                        quantity=Quantity(
                            unit=OntologyClass(id='UCUM:mg.kg-1', label='milligram per kilogram'),
                            value=0.4,
                        ),
                        schedule_frequency=OntologyClass(id='NCIT:C64576', label='Once'),
                        interval=TimeInterval(
                            start=Timestamp.from_str('2020-09-02T00:00:00Z'),
                            end=Timestamp.from_str('2020-09-02T00:00:00Z'),
                        )
                    ),
                )
            ),
            treatment_target=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            treatment_intent=OntologyClass(id='NCIT:C62220', label='Cure'),
            adverse_events=(
                OntologyClass(id='HP:0025637', label='Vasospasm'),
            ),
            treatment_termination_reason=OntologyClass(id='NCIT:C41331', label='Adverse Event')
        ),
        MedicalAction(
            action=TherapeuticRegimen(
                identifier=OntologyClass(id='NCIT:C10894', label='Carboplatin/Etoposide/Vincristine'),
                start_time=TimeElement(
                    element=Age(iso8601duration='P7M'),
                ),
                end_time=TimeElement(
                    element=Age(iso8601duration='P8M'),
                ),
                regimen_status=TherapeuticRegimen.RegimenStatus.COMPLETED,
            ),
            treatment_target=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            treatment_intent=OntologyClass(id='NCIT:C62220', label='Cure'),
        ),
        MedicalAction(
            action=Procedure(
                code=OntologyClass(id='NCIT:C48601', label='Enucleation'),
                body_site=OntologyClass(id='UBERON:0004548', label='left eye'),
                performed=TimeElement(element=Age(iso8601duration='P8M2W'))
            ),
            treatment_target=OntologyClass(id='NCIT:C7541', label='Retinoblastoma'),
            treatment_intent=OntologyClass(id='NCIT:C62220', label='Cure'),
        ),
    )


@pytest.fixture(scope='package')
def files() -> typing.Sequence[File]:
    return (
        File(
            uri='file://data/germlineWgs.vcf.gz',
            individual_to_file_identifiers={
                'proband A': 'sample1',
                'proband B': 'sample2'
            },
            file_attributes={
                'fileFormat': 'VCF',
                'genomeAssembly': 'GRCh38',
            },
        ),
        File(
            uri='file://data/somaticWgs.vcf.gz',
            individual_to_file_identifiers={
                'proband A': 'sample1',
                'proband B': 'sample2'
            },
            file_attributes={
                'fileFormat': 'VCF',
                'genomeAssembly': 'GRCh38',
            },
        ),
    )


@pytest.fixture(scope='package')
def meta_data() -> MetaData:
    """
    `MetaData` from the `retinoblastoma` phenopacket.
    """
    return MetaData(
        created=Timestamp.from_str('2021-05-14T10:35:00Z'),
        created_by='anonymous biocurator',
        submitted_by=None,
        resources=(
            Resource(
                id='hp', name='human phenotype ontology',
                url='http://purl.obolibrary.org/obo/hp.owl',
                version='2021-08-02', namespace_prefix='HP',
                iri_prefix='http://purl.obolibrary.org/obo/HP_'
            ),
            Resource(
                id='geno', name='Genotype Ontology',
                url='http://purl.obolibrary.org/obo/geno.owl',
                version='2020-03-08', namespace_prefix='GENO',
                iri_prefix='http://purl.obolibrary.org/obo/GENO_'
            ),
            Resource(
                id='ncit', name='NCI Thesaurus',
                url='http://purl.obolibrary.org/obo/ncit.owl',
                version='VERSION', namespace_prefix='NCIT',
                iri_prefix='http://purl.obolibrary.org/obo/NCIT_'
            ),
            Resource(
                id='uberon', name='Uber-anatomy ontology',
                url='http://purl.obolibrary.org/obo/uberon.owl',
                version='VERSION', namespace_prefix='UBERON',
                iri_prefix='http://purl.obolibrary.org/obo/UBERON_'
            ),
            Resource(
                id='loinc', name='Logical Observation Identifiers Names and Codes',
                url='https://loinc.org',
                version='VERSION', namespace_prefix='LOINC',
                iri_prefix='https://loinc.org'
            ),
            Resource(
                id='drugcentral', name='Drug Central',
                url='https://drugcentral.org/',
                version='VERSION', namespace_prefix='DrugCentral',
                iri_prefix='https://drugcentral.org/drugcard'
            ),
            Resource(
                id='ucum', name='Unified Code for Units of Measure',
                url='https://ucum.org',
                version='2.1', namespace_prefix='UCUM',
                iri_prefix='https://ucum.org/'
            ),
        ),
        phenopacket_schema_version='2.0.0',
    )
