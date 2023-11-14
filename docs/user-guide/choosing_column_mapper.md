# Choosing a column mapper

pyphetools defines several ColumnMapper's that map the contents of a specific column to HPO annotations.
In addition, there are AgeMapper, SexMapper, and VariantMapper classes that help to ingest this type of data but are not covered here.

To choose a ColumnMapper for a specific column, see the following table. Detailed documentation about each mapper is linked.


| Column Mapper           |   Scope                                                       |
|:------------------------|:--------------------------------------------------------------|
| [Simple column mapper](simple_column_mapper.md)  |  A column describes a sinle abnormality (HPO term) and contains symbols that represent `observed`, `excluded`, and `not measured/not available` |
| [Constant column mapper](constant_column_mapper.md) | A column for which all individuals (i.e., all rows) have a given HPO term (or the exclusion of the term) |
| [Option column mapper](option_column_mapper.md) | A column that contains several phentypic abnormalities, usually all in one organ system. |
| [Threshold column mapper](threshold_column_mapper.md)  | A column that contains a number that implies an abnormality (HPO term) if the number is above (or below) a given threshold. |



It is advisable to review several notebooks in the [Phenopacket-Store](https://github.com/monarch-initiative/phenopacket-store){:target="\_blank"} project to get a feeling for how and when to use the various mappers.