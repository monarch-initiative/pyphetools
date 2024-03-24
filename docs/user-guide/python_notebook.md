# Python (Jupyter) notebook for the Excel template

The following sections explain how to use Python code to create phenopackets from data stored using the [Excel template](excel.md).


## Preparing the notebook.

We first import the TemplateImporter to import the data and create phenopackets, and several classes to visualize the data.

```python
from pyphetools.creation import TemplateImporter
from pyphetools.visualization import IndividualTable, QcVisualizer
from IPython.display import display, HTML
import pyphetools
print(f"Using pyphetools version {pyphetools.__version__}")
```

Import the [Human Phenotype Ontology (HPO)](https://hpo.jax.org/app/) hp.json file. Note that here we show code that assumes that the file is available in the enclosing directory. Update the ORCID identifier to your own [ORCID](https://orcid.org/){:target="_blank"}  id. Indicate
the location of the template file.

```python
template = "input/BRD4_individuals.xlsx"
hp_json = "../hp.json"
created_by = "0000-0002-0736-9199"
```

import the template file. The code returns the pyphetools Individual objects, each of which contains all of the information needed to create a phenopacket and which here can be used if desired for debugging or further analysis. The cvalidator object is used to display quality assessment information.

```
timporter = TemplateImporter(template=template, hp_json=hp_json, created_by=created_by)
individual_list, cvalidator = timporter.import_phenopackets_from_template()
```
Display quality assessment data.
```
qc = QcVisualizer(cohort_validator=cvalidator)
display(HTML(qc.to_summary_html()))
```
Display summaries of each phenopacket. The command ``cvalidator.get_error_free_individual_list()``returns versions of the Individual objects
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
timporter.create_hpoa_from_phenopackets(pmid=pmid, moi="Autosomal recessive")
```
or

```python
pmid = "PMID:36333996"
timporter.create_hpoa_from_phenopackets(pmid=pmid, moi="Autosomal recessive", target="OMIM:620427")
```
