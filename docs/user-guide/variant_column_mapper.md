# VariantColumnMapper

TODO -- update

ColumnMapper for columns that contain information about the variant(s) found in an individual.
There are two main ways of using this class. If there is a column that contains an HGVS expression
for the variant (without the transcript), then the transcript is indicated by the default_transcript argument.




```python title="ThresholdedColumnMapper constructor"
transcript='NM_015133.4'
varMapper = VariantColumnMapper(assembly='hg38',
                                variant_column_name='Transcript:NM_015133.4',
                                transcript=transcript, 
                                default_genotype='heterozygous')                        
```
The VariantColumnMapper is now ready to go to map HGVS expressions in the column ``Transcript:NM_015133.4``.




##  Manual assignment of variants

In some cases, other symbols are used, and then we create the Variant objects manually and assign them
using a map.



```python title="ThresholdedColumnMapper constructor"
genome = 'hg38'
default_genotype = 'heterozygous'
transcript='NM_014159.7'
varMapper = VariantColumnMapper(assembly=genome,column_name='Variant',
                              transcript=transcript, default_genotype=default_genotype)
variant_5218 = varMapper.map_cell('c.5218C>T')
variant_5219 = varMapper.map_cell('c.5219G>A')
variant_map = {"p.(Arg1740Trp)": variant_5218, 'p.(Arg1740Gln)': variant_5219}
varMapper.set_variant_symbol_dictionary(variant_map)
```