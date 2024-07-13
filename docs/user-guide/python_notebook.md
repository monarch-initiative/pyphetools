# Python (Jupyter) notebook for the Excel template

The following sections explain how to use Python code to create phenopackets from data stored using the [Excel template](excel.md).


## Preparing the notebook.

We first import the TemplateImporter to import the data and create phenopackets, and several classes to visualize the data.

```python
from pyphetools.creation import TemplateImporter, Moi
from pyphetools.visualization import IndividualTable, QcVisualizer
from IPython.display import display, HTML
import pyphetools
print(f"Using pyphetools version {pyphetools.__version__}")
```

### Set paths and identifiers
Update the ORCID identifier to your own [ORCID](https://orcid.org/){:target="_blank"}  id. 
Update the path to the template file.

```python
template = "input/BRD4_individuals.xlsx"
created_by = "0000-0002-0736-9199"
```

### Import the template file. 
The code returns the pyphetools Individual objects, each of which contains all of the information needed to create a phenopacket and which here can be used if desired for debugging or further analysis. The cvalidator object is used to display quality assessment information.
Note that optionally you can provide an argument to the location of the hp.json file using the ``hp_json``argument. If no argument is provided, the hpo-toolkit library will download the latest version of
hp.json to your user directory (.hpotk folder).

```python
timporter = TemplateImporter(template=template,  created_by=created_by)
individual_list, cvalidator = timporter.import_phenopackets_from_template()
```

### Structural variants
pyphetools will automatically retrieve information about small variants coded as HGVS strings using the
[VariantValidator](https://variantvalidator.org/) API. Until very recently, it was challenging to determine the exact positions of larger structural variants, and for this reason, publications often described them
using phrases such as "whole gene deletion" or "EX9-12DEL". If such as string is found in the template file,
pyphetool will emit an error such as the following.

<figure markdown>
![Validation results](../img/deletion_error.png){ width="1000" }
<figcaption>Validation Results.
</figcaption>
</figure>

This can be fixed by passing an argument with a set of all strings that represent deletions (as in the following example), duplications, or inversions.

```python title="Specifying structural variants"
del_set = {"EX9-12DEL"}
timporter = TemplateImporter(template=template, created_by=created_by)
individual_list, cvalidator = timporter.import_phenopackets_from_template(deletions=del_set)
```

### Display quality assessment data.
```
qc = QcVisualizer(cohort_validator=cvalidator)
display(HTML(qc.to_summary_html()))
```
### Display summaries of each phenopacket. 

The command ``cvalidator.get_error_free_individual_list()``returns versions of the Individual objects
in which errors such as redundancies have been removed; this is the data that gets transformed into phenopackets.


```python
table = IndividualTable(cvalidator.get_error_free_individual_list())
display(HTML(table.to_html()))
```

### HPOA files

If desired, we can transform the phenopacket data into an HPOA file. This is the format that the HPO team uses to create the phenotype.hpoa file that is distributed on the [Human Phenotype Ontology](https://hpo.jax.org/){target="_blank"} website. We need to choose a PubMed identifier that documents
the mode of inheritance (MOI) and then indicate the MOI. If multiple distinct diseases are stored in the phenopackets directory, then we need to choose one of them using the target argument.

Check results of variant encoding.
```python
pmid = "PMID:36333996"
df = timporter.create_hpoa_from_phenopackets(pmid=pmid, mode_of_inheritance=Moi.AR)
```
or

```python
pmid = "PMID:36333996"
df = timporter.create_hpoa_from_phenopackets(pmid=pmid, mode_of_inheritance=Moi.AD, target="OMIM:620427")
```
