.. _option_column_mapper:

==================
OptionColumnMapper
==================

Mapper to be used if the column has a set of defined items but text mining is not required.

.. code-block:: python
  :linenos:

  other_d = {
    "HP": ["High palate", "HP:0000218"],
    "D": ["Dolichocephaly", "HP:0000268"],
    "En": ["Deeply set eye", "HP:0000490"], # i.e., Enophthalmus
    "DE": ["Dural ectasia", "HP:0100775"],
    "St": ["Striae distensae", "HP:0001065"]
  }
  otherMapper = OptionColumnMapper(concept_recognizer=hpo_cr, option_d=other_d)

This mapper will recognize ``HP`` as well as ``HP,D,St``. The mapper interprets
``,``,  ``;``, ``|``, and ``/`` as delimiters. Note that the value of the dictionary
can be either a two-element array as shown above or a simple string that must be the
label of the HPO term.

If text-mining is required, use the :ref:`custom_column_mapper`.
