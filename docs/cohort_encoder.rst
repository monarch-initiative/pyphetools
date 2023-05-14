.. _cohort_encoder:

=============
CohortEncoder
=============

This class coordinates the extract-transform-load (ETL) operations for a cohort, usually taken from 
a table in a publication or supplemental file. It is intended to be used with the ColumnMappers to map
each relevant column of the table.



.. code-block:: python
  :linenos:

  pmid = "PMID:30612693"
  encoder = CohortEncoder(df=dft, hpo_cr=hpo_cr, column_mapper_d=column_mapper_d, 
                          individual_column_name="patient_id", 
                          agemapper=ageMapper, 
                          sexmapper=sexMapper,
                          metadata=metadata,
                          variant_mapper=varMapper,
                          pmid=pmid)
  disease_id = "OMIM:618443"
  disease_label = "Neurodevelopmental disorder with or without variable brain abnormalities"
  encoder.set_disease(disease_id=disease_id, label=disease_label)
  # optionally get the objects and display the phenopackets, for debugging
  individuals = encoder.get_individuals()
  i1 = individuals[0]
  phenopacket1 = i1.to_ga4gh_phenopacket(metadata=metadata.to_ga4gh())
  json_string = MessageToJson(phenopacket1)
  print(json_string)
  # output all encoded phenopackets
  output_directory = "phenopackets"
  encoder.output_phenopackets(outdir=output_directory)
  # optionally, in Jupyter notebooks, show a phenopacket for debugging
  ! cat phenopackets/example.json