# SimpleColumnMapper


ColumnMapper for columns that contain information about a single phenotypic abnormality only.
This kind of ColumnMapper should be used for columns that can be representing by one HPO term
and which can contain symbols such as "+_" "Y", "yes" indicating that the abnormality was
observed, symbols such as "-", "N", "no" indicating that the abnormality was explicity excluded
and (optionally) symbols indicating that the abnormality was not measured or assessed.

For instance, the following mapper would generate a phenotypic feature for
[Global developmental delay](https://hpo.jax.org/app/browse/term/HP:0001263){:target="\_blank"} if the
column contains "yes" (observed) and would call it as excluded if the column contains "no".
For any other text or for an empty cell, the feature would be called as not measured (and would
not be included in the phenopacket).


```python title="SimpleColumnMapper constructor"
  ddMapper = SimpleColumnMapper(hpo_id='HP:0001263',
    hpo_label='Global developmental delay',
    observed='yes',
    excluded='no')
```



It can be convenient to add multiple SimpleColumnMappers at the same time. The following function enables this.



```python title="Creating multiple SimpleColumnMapper objects at once"
## Note that we previously have created an HPO Concept Recognizer object
parser = HpoParser()
hpo_cr = parser.get_hpo_concept_recognizer()
##
column_mapper_d = {}
items = {
    'regression': ["Developmental regression","HP:0002376"],
    'autism': ['Autism', 'HP:0000717'],
    'hypotonia': ['Hypotonia', 'HP:0001252'],
    'movement disorder': ['Abnormality of movement', 'HP:0100022'],
    'CVI': ['Cerebral visual impairment', 'HP:0100704'], 
    'seizures': ['Seizure','HP:0001250'],
    'DD': ['Global developmental delay', 'HP:0001263']
}
item_column_mapper_d = hpo_cr.initialize_simple_column_maps(column_name_to_hpo_label_map=items, 
                            observed='yes',
                            excluded='no')
# Transfer to column_mapper_d
for k, v in item_column_mapper_d.items():
    column_mapper_d[k] = v
```
