"""
A package with strongly typed Phenopacket Schema types and the code for I/O and validation.

Examples
^^^^^^^^

Create phenopacket programatically
##################################

We recommend to bring the classes into scope all at once using the import star:

>>> from pyphetools.pp.v202 import *

Then, we can build a phenopacket from the individual building blocks.

Let's start with the subject:

>>> subject = Individual(
...   id='proband A',
...   time_at_last_encounter=TimeElement(
...     element=Age(iso8601duration='P6M'),
...   ),
...   sex=Sex.FEMALE,
... )
>>> subject.id
'proband A'
>>> subject.sex.name
'FEMALE'

The created subject represents a female proband who had 6 months at the time of the last encounter.

We can update the fields using a simple assignment:

>>> subject.karyotypic_sex = KaryotypicSex.XX
>>> subject.karyotypic_sex.name
'XX'

We assigned an enum constant `KaryotypicSex.XX` to  previously unset `karyotypic_sex` attribute.


The same can be done with object attributes:

>>> subject.vital_status = VitalStatus(
...   status=VitalStatus.Status.DECEASED,
...   time_of_death=TimeElement(
...     element=Age(iso8601duration='P1Y')
...   ),
...   cause_of_death=OntologyClass(
...     id='NCIT:C7541', label='Retinoblastoma',
...   ),
... )

We set the vital status to indicate that the proband died at 1 year of age due to *Retinoblastoma*.

Now we can create a phenopacket. The phenopacket requires an identifier, `MetaData` and an optional subject.

>>> pp = Phenopacket(
...   id='example.retinoblastoma.phenopacket.id',
...   meta_data=MetaData(
...     created=Timestamp.from_str('2021-05-14T10:35:00Z'),
...     created_by='anonymous biocurator',
...   ),
... )

To create a phenopacket, we must provide the  `id` and `meta_data` fields
since they are required by the Phenopacket Schema.
The same applies to `created` and `created_by` fields of `MetaData`.

`MetaData` contextualizes the used ontology classes, such as `NCIT:C7541` *Retinoblastoma*,
to a particular ontology, such as NCI Thesaurus. We can store the ontology resource in `MetaData.resources`
field:

>>> pp.meta_data.resources.append(
...   Resource(
...     id='ncit', name='NCI Thesaurus', url='http://purl.obolibrary.org/obo/ncit.owl',
...     version='23.09d', namespace_prefix='NCIT', iri_prefix='http://purl.obolibrary.org/obo/NCIT_',
...   ),
... )

All repeated elements, such as `MetaData.resources`, can be accessed via a `list`.

Read/write JSON and Protobuf
############################

We can read and write phenopackets in JSON format using the `JsonDeserializer` and `JsonSerializer` classes:

>>> from pyphetools.pp.parse.json import JsonSerializer, JsonDeserializer
>>> serializer = JsonSerializer()

The serializer can write a Phenopacket Schema building block, such as `OntologyClass` or `Phenopacket` into
a file handle:

>>> from io import StringIO
>>> buf = StringIO()
>>> serializer.serialize(subject.vital_status, buf)
>>> buf.getvalue()
'{"status": "DECEASED", "timeOfDeath": {"age": {"iso8601duration": "P1Y"}}, "causeOfDeath": {"id": "NCIT:C7541", "label": "Retinoblastoma"}}'

and the JSON can be read back from a file handle:

>>> _ = buf.seek(0)  # Rewind and ignore the result
>>> deserializer = JsonDeserializer()
>>> decoded = deserializer.deserialize(buf, VitalStatus)
>>> decoded == subject.vital_status
True

The building block can also be written into Protobuf wire format.
We can do a similar round-trip as above, but we will need a byte IO handle:

>>> from io import BytesIO
>>> byte_buf = BytesIO()

We can write the subject into the buffer and get the same data back:

>>> subject.dump_pb(byte_buf)
>>> _ = byte_buf.seek(0)  # Rewind to start
>>> other = Individual.from_pb(byte_buf)
>>> subject == other
True
"""

from . import parse
from . import v202
from ._timestamp import Timestamp

__all__ = [
    'parse',
    'v202',
    'Timestamp',
]
