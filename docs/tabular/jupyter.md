# Using pyphetools in a Jupyter notebook


This page provides an overview of how to structure a Jupyter notebook to import tabular data. We recommend importing data for one disease at a time.

### Importing necessary packages


Most notebooks will want to first import all necessary packages. It is helpful to print out the version
used (see the last two lines) in case of errors or feature requests. Sometimes, additional packages need
to be imported to support special cases.


```python title="Imports"
import pandas as pd
pd.set_option('display.max_colwidth', None) # show entire column contents, important!
from IPython.display import HTML, display
from pyphetools.creation import *
from pyphetools.validation import *
from pyphetools.visualization import *
import pyphetools
print(f"pyphetools version {pyphetools.__version__}")
```

### Import the Human Phenotype Ontology (HPO) file

It is useful to import the HPO file and create the `MetaData` object
(which records your `ORCID <https://orcid.org/>`_ id and the version of the HPO used) in one step.

The following code first creates a `Citation` object with data about the PubMed identifier and title of the paper
we are curating.
It then imports the HPO (which in this example has been previously downloaded and stored at the file location `../hp.json`). Note
that the hp.json file can be downloaded from many places including the [HPO Homepage](https://hpo.jax.org/app/){:target="_blank"}.
We recommend always using the latest version. The code then initializes the HPO concept recognizer (i.e., text-mining) object, the ontology object,
and the MetaData object (see  the
[GA4GH phenopackets documentation](https://phenopacket-schema.readthedocs.io/en/latest/){:target="\_blank"} for more details on MetaData).

```python title="Configure MetaData"
PMID = "PMID:36189931"
title = "Comprehensive genetic screening for vascular Ehlers-Danlos syndrome through an amplification-based next-generation sequencing system"
cite = Citation(pmid=PMID, title=title)
parser = HpoParser(hpo_json_file="../hp.json")
hpo_cr = parser.get_hpo_concept_recognizer()
hpo_version = parser.get_version()
hpo_ontology = parser.get_ontology()
metadata = MetaData(created_by="ORCID:0000-0002-5648-2155", citation=cite)
metadata.default_versions_with_hpo(version=hpo_version)
print(f"HPO version {hpo_version}")
```

Note that if you leave the argument of HpoParser empty, the class will download the latest version of HPO automatically. Depending on the settings
of your system, this may lead to an SSL certificate error, which can be addressed by adding the following two lines to the top of the cell
```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```



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


Data with clinical columns in typical supplemental files often have one of several formats.


1. Simple. The column header is a string such as 'ID' that corresponds to an HPO term, for instance [Intellectual disability HP:0001249](https://hpo.jax.org/app/browse/term/HP:0001249){:target="\_blank"}, whereby each cell has a symbol such as
'Y', 'y', '+', 'yes', ''n', '-', etc. to indicate whether the feature was present in the individual specified by the row.  See :ref:`simple_column_mapper` for more information about how to work with this kind of column.
2. Options. Some columns contain several strings, each of which corresponds to a specific HPO term. For instance, a columns such as 'severity of ID' with entries such as `mild`, `moderate`, `severe` would correspond to HPO terms for
`Intellectual disability, mild HP:0001256 <https://hpo.jax.org/app/browse/term/HP:0001256>`_, etc. See :ref:`option_column_mapper` for more information about how to work with this kind of column.
3. Constant. This mapper can be used if all individuals diusplay the same feature. See :ref:`simple_column_mapper`.
4. Threshold. This can be used for columns that have numerical data whereby being above or below a certain threshold is abnormal. See :ref:`threshold_column_mapper`.


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


## Mapping the data

Unfortunately, tabular data as it is currently available is so hetgerogeneous, that it is difficult to provide a simple step-for-step recipe for
how to use pyphetools to encode it. The basic steps are to choose a column mapper type for each of the phenotype columns in the table, and to use
age, sex, and variant column mappers for these types.

- HPO (phenotype) [column mapper types](choosing_column_mapper.md)
- Variants: [variant column mapper](variant_column_mapper.md)
- Age of onset and age at last examination: TODO
- Sex column mapper: TODO

We recommend studying available notebooks in the [phenopacket-store](https://github.com/monarch-initiative/phenopacket-store){:target:"_blank"} to get an idea of how to combine the column mappers for several examples.

## Cohort encoder

The [CohortEncoder](../api/creation/cohort_encoder.md) class was designed to work with the above column mappers. It can be setup as follows.

```python title="Setting up the cohort mapper"
encoder = CohortEncoder(df=df,
                        hpo_cr=hpo_cr,
                        column_mapper_list=column_mapper_list,
                        individual_column_name="individual_id",
                        age_of_onset_mapper=onsetMapper,
                        age_at_last_encounter_mapper=lastEncounterMapper,
                        sexmapper=sexMapper,
                        variant_mapper=varMapper,
                        metadata=metadata)
```
Note that the ``age_of_onset_mapper`` and ``age_at_last_encounter_mapper`` arguments can be omitted if this information is not available.

## Specify the disease

pyphetools requires a disease identifier and label, as follows.

```python title="Specify the disease"
vEDS = Disease(disease_id='OMIM:130050', disease_label='Ehlers-Danlos syndrome, vascular type')
encoder.set_disease(vEDS)
```

## Validation

Now we can retrieve the Individual objects and do Q/C


```python title="pyphetools validation"
individuals = encoder.get_individuals()
cvalidator = CohortValidator(cohort=individuals, ontology=hpo_ontology, min_hpo=1, allelic_requirement=AllelicRequirement.MONO_ALLELIC)
qc = QcVisualizer(cohort_validator=cvalidator)
display(HTML(qc.to_summary_html()))
```

This step will show warnings that can generally be ignored (e.g., the redundant terms were removed). If there are serious errors, a message will be shown, and the user will need to fix the errors before going on.

## Summaries of the phenopackets

The following commands display a table with a summary of each phenopacket created.
```python title="List of phenopackets created in the current notebook"
individuals = cvalidator.get_error_free_individual_list()
table = PhenopacketTable(individual_list=individuals, metadata=metadata)
display(HTML(table.to_html()))
```
## Saving phenopackets to file
The following command writes each phenopacket as a JSON file to the directory ``phenopackets``(other directory names can be chosen).

```python title="output"
Individual.output_individuals_as_phenopackets(individual_list=individuals,
                                              metadata=metadata)
```



## HPOA files
To create the HPOA files used to create the phenotype.hpoa by the HPO team, adapt the following code. Note that this code is
slightly different to the code used with the Excel template to build HPOA files.

Please see [HPOA files](../developers/hpoa_editing.md).