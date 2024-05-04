# Data-Entry Template

pyphetools offers two main ways to encode clinical data as phenopackets. The library provides various functions to encode data found in
typical supplementary materials of publications about cohorts. This option, which is covered in more detail [here](../developers/developers.md) is intended for those
with skills in scripting with Python. Additionally, pyphetools can ingest data encoded in an Excel template that can be used without additional scripting.
The template can be ingested using a standardized notebook. Alternatively, users are invited to work with the HPO team to enter the data into the HPO database.

See [here](https://monarch-initiative.github.io/phenopacket-store/){:target="\_blank"} for many examples of how to use the template.


## Template Creation

Excel templates can be  created in a Jupyter notebook to prepopulate them with the HPO terms, gene and disease ids.

We will show an example for creating a template for
[Simpson-Golabi-Behmel syndrome, type 2-OMIM:300209](https://omim.org/entry/300209).


```python
from pyphetools.creation import TemplateCreator
```

First initialize the creator object with the path to a ``hp.json`` file (adjust the path as needed on your system).

```python
tcreator = TemplateCreator(hp_json="../hp.json")
```

We will then use HPO text mining to retrieve as many terms as possible from a description of the phenotypic features that can be derived from the article you are curating or any relevant source. We took the following description from [Tenorio J, et al., Simpson-Golabi-Behmel syndrome types I and II. Orphanet J Rare Dis. 2014](https://pubmed.ncbi.nlm.nih.gov/25238977/){:target="_blank"}

```python
tcreator.add_seed_terms("""
It is an infantile lethal variant of SGBS associated with hydrops fetalis.
In the first report, the authors reported 4 maternally-related male cousins
with a severe variant of SGBS [6]. One of these males was aborted therapeutically
at 19 weeks of gestation following the detection of multicystic kidneys on ultrasound.
The three live born males were hydropic at birth. They also depicted craniofacial
anomalies including macrocephaly; apparently low-set, posteriorly angulated ears; hypertelorism;
short, broad nose with anteverted nares; large mouth with thin upper vermilion border;
prominent philtrum; high-arched and cleft palate. Other findings were short neck;
redundant skin; hypoplastic nails; skeletal defects involving upper and lower limbs;
gastrointestinal and genitourinary anomalies, hypotonia and neurologic impairment.
""")```

The script added 14 HPO terms to the template. Now we specify the remaining information.

```python
disease_id = "OMIM:300209"
disease_label = "Simpson-Golabi-Behmel syndrome, type 2"
symbol = "OFD1"
hgnc_id = "HGNC:2567"
ofd1_transcript='NM_003611.3'
tcreator.create_template(disease_id=disease_id,
                         disease_label=disease_label,
                         gene_symbol=symbol,
                         HGNC_id=hgnc_id,
                         transcript=ofd1_transcript)
```

The following snippet can be used as a "starter" by pasting it into the notebook.

```python title="Starter"
tc.create_template(disease_id="",
                         disease_label="",
                         gene_symbol="",
                         HGNC_id="",
                         transcript=""
```)


The script creates a file that can be opened in Excel and used for curation. Add additional HPO terms as necessary and remove terms that are not needed.