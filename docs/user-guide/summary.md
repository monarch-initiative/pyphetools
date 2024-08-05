# Summary

The pyphetools library provides code to create a summary of all of the phenopackets of a cohort. This can be useful to review work or understand the distribution of data. This page explains how to set up the notebook.


## Imports

We first import several classes to visualize the data.

```python
import pandas as pd
pd.set_option('display.max_colwidth', None) # show entire column contents, important!
from IPython.display import HTML, display
from pyphetools.visualization import *
import pyphetools
print(f"Using pyphetools version {pyphetools.__version__}")
```

## Extract phenopackets
We then extract a list of phenopackets from the target directory.

```python
ingestor = PhenopacketIngestor(indir="phenopackets")
ppkt_list = ingestor.get_phenopacket_list()
```
By default, pyphetools will create a new directory called **phenopackets** into which it will write the new phenopackets. Therefore, the PhenopacketIngestor will use **phenopackets** as a default if we do not specify the "indir" argument.
```python
ingestor = PhenopacketIngestor()
ppkt_list = ingestor.get_phenopacket_list()
```

If the input directory contains phenopackets for more than one disease, an error message will appear. In this case, use the **disease_id** argument to specific the disease identifier.


## Detailed table
The following command will display a table with the counts of annotated HPO terms for each PubMed identifier (publication) used in the cohort.

```python
detailed_table = DetailedSupplTable(patient_list=ppkt_list)
display(HTML(detailed_table.get_html_table_by_pmid(min_count=1)))
```


## pcharts

The **PhenopacketCharts** class uses matplotlib to display barcharts to show salient aspects of the data

This will display a chart with the counts of each disease in the cohort.

```python
pcharts = PhenopacketCharts(indir="phenopackets")
pcharts.disease_barchart();
```



This will display a chart with the counts of individuals per publication (PMID) in the cohort.

```python
pcharts.pmid_barchart();
```

And finally, this will display a chart with the most commonly annotated HPO terms in the cohort.

```python
pcharts.most_common_hpo_terms(max_terms_to_show=10);
```
