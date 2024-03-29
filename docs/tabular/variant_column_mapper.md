# VariantColumnMapper

TODO -- update

ColumnMapper for columns that contain information about the variant(s) found in an individual.
There are two main ways of using this class. If there is a column that contains an HGVS expression
for the variant (without the transcript), then the transcript is indicated by the default_transcript argument.


# HGVS vs Structural

pyphetools uses two different classes to ingest small variants (which must be encoded using valid
[HGVS notation](https://varnomen.hgvs.org/){:target="\_blank"} or structural variants (which are not validated).


### HGVS

The following code can be adapted to read HGVS-encoded variants. It assumes that there is
a column in the input table called *Variant*. It first extracts a list of unique variants,
and used [variant validator](https://variantvalidator.org/) to check them and to retrieve additional 
data such as the chromosomal position. The resulting *Variant* object is placed in a dictionary together
with the original string used in the table (if necessary, one can correct minor errors such as the failure to
use the "c." below).

```python title="Calling Variant Validator for HGVS-encoded variants"
hg38 = 'hg38'
default_genotype = 'heterozygous'
WFS1_transcript='NM_006005.3'
vvalidator = VariantValidator(genome_build=hg38, transcript=WFS1_transcript)
variant_list = df['Variant'].unique()
print(variant_list)
variant_d = {}
for v in variant_list:
    if v == "1380del9":
        hgvs = "c.1385_1393del"
    else:
        hgvs = f"c.{v}"
    var = vvalidator.encode_hgvs(hgvs)
    variant_d[v] = var
```

For structural variants, pyphetools enocdes the variant using corresponding classes from Sequence Ontology with
the *StructuralVariant* class, which has the static functions

- chromosomal_deletion
- chromosomal_duplication
- chromosomal_inversion

as well as a constructor that can take any relevant sequence ontology class.


```python title="chromosomal deletion"
sv = StructuralVariant.chromosomal_deletion(cell_contents="46,XY.ish del(7)(p14.1)(RP11-816F16-)", 
````````````````````````````````````````````gene_id="HGNC:4319", 
                                            gene_symbol="GLI3")
```
The cell contents argument contains the variant name as used in the original table.

It is possible to mix HGVS and structural variants in Python code. An example follows.
```python title="HGVS and structural variants"
struct_variants = { "rsa7p14.1(kit P179)x1",
                    "46,XY.ish del(7)(p14.1)(RP11-816F16-)",
                    "46,XX.ish del(7)(p14.1p14.1)(GLI3-)" }
gli3_symbol = "GLI3"
gli3_id = "HGNC:4319"
gli3_variants = df1['cDNA alteration'].unique()
gli3_variant_d = {}
for gli3v in gli3_variants:
    if gli3v in struct_variants:
        sv = StructuralVariant.chromosomal_deletion(cell_contents=gli3v, gene_id=gli3_id, gene_symbol=gli3_symbol)
        print(gli3v)
        gli3_variant_d[gli3v] = sv
    else:
        v = hgvsMapper.encode_hgvs(gli3v)
        gli3_variant_d[gli3v] = v
```

## VariantColumnMapper

One the dictionary of variants has been constructed as above, we create the variant mapper as follows.

```python title="VariantColumnMapper constructor"
variantMapper = VariantColumnMapper(variant_d=gli3_variant_d,
                                    variant_column_name="cDNA alteration",
                                    default_genotype='heterozygous'
                                   )                      
```
The VariantColumnMapper is now ready to go to map HGVS expressions in the column "cDNA alteration".



