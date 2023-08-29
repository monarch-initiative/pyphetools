.. _custom_column_mapper:

==================
CustomColumnMapper
==================

Column mapper for concept recognition (CR) augmented by custom maps for
concepts missed by automatic CR.

This column mapper should be used for columns that contain free text representing multiple
different phenotypic abnormalities. As a rule, most of these will be captured by
text mining (concept recognition). We use the ``preview_column`` function to assess
the performance of the mapper, and if concepts are missed, they can be added
using the optional ``custom_map_d`` argument. In some cases, concept recognition picks up terms that we deem to be
false positive or irrelevant. In this case, we can add the strings to the optional
``excluded_set`` argument to cause them to be skipped by the mapper.


.. code-block:: python
  :linenos:

  prenatal_custom_map = {'agenesis of the corpus callosum': 'Agenesis of corpus callosum',
                         '\nIUGR': 'Intrauterine growth retardation',
                         'small cerebellum':'Cerebellar hypoplasia',
                         'vsd': 'Ventricular septal defect',
                        }
  excluded = {'maternal asthma'}
  prenatalMapper = CustomColumnMapper(concept_recognizer=hpo_cr,
                                      custom_map_d=prenatal_custom_map,
                                      excluded_set=excluded)
  prenatalMapper.preview_column(dft['Prenatal complications'])

