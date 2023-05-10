.. _variant_column_mapper:

===================
VariantColumnMapper
===================

ColumnMapper for columns that contain information about the variant(s) found in an individual.
There are two main ways of using this class. If there is a column that contains an HGVS expression
for the variant (without the transcript), then the transcript is indicated by the default_transcript argument.

In some cases, other symbols are used, and then we create the Variant objects manually and assign them
using the