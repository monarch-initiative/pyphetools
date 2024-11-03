


class Disease:
    """
    Simple data object to hold ontology id/label for a disease diagnosis

    :param disease_id: a CURIE such as OMIM:600324
    :type disease_id: str
    :param disease_label: the name of the disease
    :type disease_label: str
    """

    def __init__(self, disease_id:str, disease_label):
        if " " in disease_id:
            raise ValueError(f"Malformed disease identifier with white space: \"{disease_id}\"")
        if disease_label.startswith(" ") or disease_label.endswith(" "):
            raise ValueError(f"Malformed disease label (starts/ends with whitespace): \"{disease_label}\"")
        # occasionally, copy-paste error leads to this kind of malformed label:  "Developmental and epileptic encephalopathy 50\t616457\tAR\t3\t"
        if "\t" in disease_label:
            raise ValueError(f"Malformed disease label (contains tabs): \"{disease_label}\"")
        self._id = disease_id
        self._label = disease_label


    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    def __hash__(self):
        return hash((self._id, self._label))

    def __eq__(self, other):
        return (self.id, self.label) == (other.id, other.label)

    def __repr__(self):
        return f'{self.label} ({self.id})'
