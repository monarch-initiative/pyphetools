.. _custom_column_mapper:

====================
ConstantColumnMapper
====================

Column mapper for cases where all individuals in a cohort have a certain phenotypic abnormality. If the excluded argument is set to True,
then the abnormality was excluded in all individuals. This mapper is a shortcut that appears to be useful for some supplemental files.



.. code-block:: python
  :linenos:

  hp_id =  "HP:0031956"
  hp_label = "Elevated circulating aspartate aminotransferase concentration"
  mapper = ConstantColumnMapper(hpo_id=hp_id, hpo_label=hp_label)
  hp_term_list = mapper.map_cell("n/a")


In this case, ``hp_term_list`` contains a single term corresponding to the indicated HP term (regardless of the contents of the cell). If this 
mapper is used with the CohortMapper, then all individuals in the cohort will be annotated to the term.

The following code is used if the phenotypic abnormality was explicitly excluded in all individuals in the cohort.

.. code-block:: python
  :linenos:

  hp_id =  "HP:0031956"
  hp_label = "Elevated circulating aspartate aminotransferase concentration"
  mapper = ConstantColumnMapper(hpo_id=hp_id, hpo_label=hp_label, excluded=True)
  hp_term_list = mapper.map_cell("n/a")

