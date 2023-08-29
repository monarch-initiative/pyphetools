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


Shortcut to creating option mapper objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to create the dictionaries used by the OptionColumnMapper by hand.
However, the following command will generate a code-template from which users
can copy and adapt code for relevant columns.

.. code-block:: python
   :linenos:

    dft = ... #  Pandas DataFrame with columns representing clinical data
    output = OptionColumnMapper.autoformat(df=dft, concept_recognizer=hpo_cr)
    print(output)

    post_fossa_d = {'Mega cisterna magna': 'Enlarged cisterna magna',
                    'Normal': 'PLACEHOLDER',
                    'Mega cistema magna': 'PLACEHOLDER'}
    post_fossaMapper = OptionColumnMapper(concept_recognizer=hpo_cr, option_d=post_fossa_d)
    post_fossaMapper.preview_column(df['Post fossa']))
    column_mapper_d['Post fossa'] = post_fossaMapper

    pituitary_d = {'Normal': 'PLACEHOLDER'}
    pituitaryMapper = OptionColumnMapper(concept_recognizer=hpo_cr, option_d=pituitary_d)
    pituitaryMapper.preview_column(df['Pituitary']))
    column_mapper_d['Pituitary'] = pituitaryMapper
    (...)

For instance, in the above example, there is a column called `Post fossa` in the DataFrame dft. The cell contents
for the rows of the column contained several strings that we might want to map. `Enlarged cisterna magna` was
recognized as the label of the HPO term `Enlarged cisterna magna (HP:0002280) <https://hpo.jax.org/app/browse/term/HP:0002280>`_.
We would remove the label 'Normal' (and possible code it as excluded using other commands). The 
string `Mega cistema magna` is clearly a spelling error in the original data, and so we can map it
to the string `Enlarged cisterna magna` (replace the PLACEHOLDER) so that the string will also be mapped to the HPO term.
The next column, `Pituitary`, just shows normal, and this would not be appropriate for the OptionColumnMapper, but users 
might want to use the :ref:`simple_column_mapper` to encoded that Abnormalities of the pituitary were excluded.