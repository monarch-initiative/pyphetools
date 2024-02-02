# Data-Entry Template

pyphetools offers two main ways to encode clinical data as phenopackets. The library provides various functions to encode data found in
typical supplementary materials of publications about cohorts. This option, which is covered in more detail in TODO is intended for those
with skills in scripting with Python. Additionally, pyphetools can ingest data encoded in an Excel template that can be used without additional scripting.
The template can be ingested using a standardized notebook. Alternatively, users are invited to work with the HPO team to enter the data into the HPO database.

The schema of the template consists in two rows that specify the nature of the data. There is a fixed set of columns that capture basic demographic data together with the disease, the source publication, and the variants. The second half of the template should be used to record information about
HPO terms curated from the publications.

## Fixed columns
The first (leftmost) 11 or 12 columns specify basic demographic data together with the disease, the source publication, and the variants.
The first two rows are used to specify the datatypes and should not be changed. The following tables show the first two rows together with
one example row with data extracted from a publication (We show two tables for better legibility)


|  PMID	| title	| individual_id	| Comment| 	disease_id	| disease_label|
|:-----|:-----|:-----|:-----|:-----|:-----|
| str	| str	| str	| optional|  str| 	str|	str| 	str|
| PMID:33087723| 	Early-onset autoimmunity associated with SOCS1 haploinsufficiency| 	A1|		OMIM:603597|	Autoinflammatory syndrome, familial, with or without immunodeficiency|


1. PMID (str, i.e., string): The PubMed identifier of the publication being curated.
2. title (str): The title of the publication being curated.
3. individual_id (str): The identifier of the individual being described in the original publication. This field is required. Please add ‘individual’ if the original article does not provide an identifier (if needed, individual 1, individual 2,...).
4. Comment (str): This field is provided to record additional information that will not be used for creating phenopackets but may be helpful for future reference.
5. disease_id (str). The disease identifer (e.g., ``OMIM:154700`` or  ``MONDO:0007947``).
6. disease_label (str). The name of the disease (e.g. ``Marfan syndrome``).




|  transcript| 	allele_1| 	variant.comment| 	age_of_onset| 	sex	| HPO	|
|:-----|:-----|:-----|:-----|:-----|:-----|
|  str| HGVS str|	optional|  	iso8601	| M:F:O:U| 	na	|
| NM_003745.2	|c.368C>G|	p.P123R|	P2Y|	F	|na|

7. transcript (str): The identifier of the transcript. NCBI RefSeq or ENSEMBL identifiers are preferred.
8. allele_1 (HGVS str): A string representing the first pathogenic allele (variant) according to [HGVS](https://hgvs-nomenclature.org/stable/background/simple/) nomenclature.
9. allele_2 (HGVS str): This field should not be used for monoallelic diseases (e.g. autosomal dominant, XLR), i.e., the Excel file should not contain this column. For biallelic diseases (autosomal recessive), specific the second allele (which will be the same as the first for homozygous genotypes).
10. variant.comment (str): This field is provided to record additional information that will not be used for creating phenopackets but may be helpful for future reference.
11. age_of_onset (iso8601): The age of onset of disease, recorded using [iso8601 convention](https://en.wikipedia.org/wiki/ISO_8601#Durations).
12. sex (M:F:U:O): one of M (male), female (F), other(O), or unknown (U)
13. HPO (na): This acts as a separator column to denote that all folowing columns specify HPO annotations (See below). Add the string na to each cell in this column.

### HPO Term Columns
All of the following columns denote HPO terms. The first row has the HPO term label. Be sure to use the same label as is shown on the HPO
webpage and do not chance the capitalization. The second row has the corresponding HPO id. The following table shows several examples, whereby
the individual_id column from above is shown for ease of exposition.




|individual_id |  Hepatitis  | 	Pancreatitis| 	Lymphadenopathy| 	Splenomegaly   |
|:-------------|:------------|:-------------|:-----------------|:------------------|
|              | HP:0012115  |HP:0001733    |  HP:0002716      |   HP:0001744      |
| A            | observed    | excluded     |                  | P4Y2M             |
| B            |P3Y          |              | observed       | excluded          |

Each table cell can contain either
1. observed: The phenotypic abnormality denoted by the HPO term was present
2. excluded: The phenotypic abnormality denoted by the HPO term was investigated and ruled out.
3. An [iso8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) string denoting the age of onset.
4. empty (blank): Not measured or no information available.

In this example, individual A was observed to have hepatitis (but age of onset is unknown or not available), pancreatitis was ruled out, no information is available about lymphadenopathy, and splenomegaly was first observed at age 4 years and 2 months.

Individual B was found to have hepatitis first observed at age 3 years, no information was available about pancreatitis, lymphadenopathy was observed (but age of onset is unknown or not available), and splenomegaly  was ruled out.









