# Using pyphetools in a Jupyter notebook

This option is intended for people who are comfortable using Python scripting, and is designed to import tabular data such as is commonly found in the supplemental files of medical publications about cohorts of individuals diagnosed with a certain disease. See also the instructions for using an [Excel template](template.md) for entering data with a minimum of scripting.


The best way to get a feeling for how to work with pyphetools is to examine the various notenooks in the
[phenopacket-store](https://github.com/monarch-initiative/phenopacket-store){:target="\_blank"} repository.

This tutorial provides some general tips for how to use the library. The library is intended to be used in a Jupyter notebook environment so that users can check intermediate results.
There are many ways of setting this up, but here is one that we often use.



```bash title="installing jupyter and running pyphetools in a notebook"
python3 -m venv your_env
source your_env/bin/activiate
pip install --upgrade pip
pip install pyphetools
pip install jupyter ipykernel
python3 -m ipykernel install --name your_env --user
jupyter-notebook
```

The virtual environment (here *your_env*) can be named as desired. The last line opens a Jupyter Notebook page;
create a new Notebook and choose the kernel called *your_env* (or whatever you called it).



### Importing necessary packages


Most notebooks will want to first import all necessary packages. It is helpful to print out the version
used (see the last two lines) in case of errors or feature requests. Sometimes, additional packages need
to be imported to support special cases.


```python title="imports"
import pandas as pd
pd.set_option('display.max_colwidth', None) # show entire column contents, important!
from IPython.display import display, HTML
from pyphetools.creation import *
from pyphetools.visualization import *
from pyphetools.validation import *
import pyphetools
print(f"Using pyphetools version {pyphetools.__version__}")
```




### Import the Human Phenotype Ontology (HPO) file


It is useful to import the HPO file and create the MetaData object (which records your `ORCID <https://orcid.org/>`_ id and the version of the HPO used) in one step.

```python title="HPO and MetaData"
parser = HpoParser()
hpo_cr = parser.get_hpo_concept_recognizer()
hpo_version = parser.get_version()
hpo_ontology = parser.get_ontology()
PMID = "PMID:16783569"
title = "A novel X-linked recessive mental retardation syndrome comprising macrocephaly and ciliary dysfunction is allelic to oral-facial-digital type I syndrome"
citation = TODO
metadata = MetaData(created_by="ORCID:0000-0002-5648-2155", pmid=PMID, pubmed_title=title)
metadata.default_versions_with_hpo(version=hpo_version)
print(f"HPO version {hpo_version}")
```

It is often useful to display the title and PubMed identifier of the publication from which the data come.
Simply replace the above code with the following.

```python title="HPO and MetaData (with title and PMID)"
parser = HpoParser()
hpo_cr = parser.get_hpo_concept_recognizer()
hpo_version = parser.get_version()
PMID = "PMID:24736735"
title = "New insights into genotype-phenotype correlation for GLI3 mutations"
metadata = MetaData(created_by="", pmid=PMID, pubmed_title=title)
metadata.default_versions_with_hpo(version=hpo_version)
```


The MetaData is a message of the GA4GH Phenopacket Schema. See the
[GA4GH phenopackets documentation](https://phenopacket-schema.readthedocs.io/en/latest/){:target="\_blank"} for more details.


### Importing the data


In general, we have taken the input data from Excel files or from CSV (command-separated value) files or TSV (tab-separated value files). Excel files can be imported using the following pandas command.

```python title="Reading an Excel input file"
df = pd.read_excel('some/path/my_supplement.xlsx')
```

Standard pandas functions are available to read CSV and TSV files. We refer to the [pandas documentation](https://pandas.pydata.org/) for  more details.


### Inspecting the input data


Users will need to carefully inspect the input table (e.g. a Supplemental file) and determine which columns or rows contain the individual id, age, and sex, the variants, and clinical information that can be encoded using HPO terms.
We recommand inspecting the first several rows using

```python title="Inspecting the data"
df.head()
```

It is also useful to look at the column names.

```python title="Inspecting the column names"
df.columns
```



## Clinical columns
pyphetools expects to get a dictionary whose keys correspond to the column names used by the pandas DataFrame,
and the values are the corresponding ColumnMapper objects. pyphetools offers different types of ColumnMapper objects, whose goal is to
encode the id, age, sex, variants, and clinical information encoded by HPO terms. We first create a dictionary whose keys should be the
names (strings) of the columns of the table and whose values are the corresponding ColumnMapper objects that we need to create for each column we
want to map. Note that it is not necessary to map each column of a table.


Data with clinical columns in typical supplemental files often have one of three forms.


1. Simple. The column header is a string such as 'ID' that corresponds to an HPO term
2. ([Intellectual disability HP:0001249](https://hpo.jax.org/app/browse/term/HP:0001249){:target="\_blank"} and each cell has a symbol such as
'Y', 'y', '+', 'yes', ''n', '-', etc. to indicate whether the feature was present in the individual specified by the row.  See :ref:`simple_column_mapper` for more information about how to work with this kind of column.
3. Options. Some columns contain several strings, each of which corresponds to a specific HPO term. For instance, a columns such as 'severity of ID' with entries such as `mild`, `moderate`, `severe` would correspond to HPO terms for
`Intellectual disability, mild HP:0001256 <https://hpo.jax.org/app/browse/term/HP:0001256>`_, etc. See :ref:`option_column_mapper` for more information about how to work with this kind of column.
4. Custom. This mapper is used for columns whose cells contain longer strings. We use a combination of text mining and specification of strings that were not matched by mining to extract HPO terms. See :ref:`custom_column_mapper_rst` for more information.
5. Constant. This mapper can be used if all individuals diusplay the same feature. See :ref:`simple_column_mapper`.
6. Threshold. This can be used for columns that have numerical data whereby being above or below a certain threshold is abnormal. See :ref:`threshold_column_mapper`.


## Row-based vs column-based

pyphetools expects the rows to represent individuals. In some cases, input files represent individuals in columns. In this case, it is necessary to transpose the table before working with pyphetools.


### Converting to row-based format

To use pyphetools, we need to have the individuals represented as rows (one row per individual) and have the items of interest be encoded as column names.
The required transformations for doing this may be different for different input data, but often we will want to transpose the table (using the pandas transpose function)
and set the column names of the new table to the zero-th row. After this, we drop the zero-th row (otherwise, it will be interpreted as an individual by the pyphetools code).



Here is an example. Other examples can be found in several of the notebooks in phenopacket-store.

```python title="Transforming from column-based to row-based format"
dft = df.transpose()
dft.columns = dft.iloc[0]
dft.drop(dft.index[0], inplace=True)
dft.head()
```


Another thing to look out for is whether the individuals (usually the first column) are regarded as the index of the table or as the first normal column.
If this is the case, it is easiest to create a new column with the contents of the index -- this will work with the pyphetools software.
An example follows -- we can now use 'patient_id' as the column name. It is easier to work with this than with the index column.



```python title="creating column with patient identifiers"
dft.index  # first check the index
dft['patient_id'] = dft.index  # Set the new column 'patient_id' to be identical to the contents of the index
dft.head() # check the transposed table
```

After this step is completed, the remaining steps to create phenopackets are the same as in the row-based notebook.
