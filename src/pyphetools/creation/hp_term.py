import pandas as pd
import phenopackets as PPKt
from .constants import Constants
import hpotk

class HpTerm:
    """
    Class to represent a phenotypic observation as an HPO term with optional modifiers

    :param hpo_id: a Human Phenotype Ontology (HPO) identifier such as HP:0001166
    :type hpo_id: str
    :param label: The HPO label that corresponds to the id (note: This class does not check for correct match)
    :type label: str
    :param observed: a boolean that indicates whether the HPO term was observed (True) or excluded (False)
    :type observed: bool
    :param measured: a boolean that indicates whether the HPO was measured (True) or not explicitly measured (False)
    :type measured: bool
    :param onset: an ISO8601 string representing the age of onset, optional
    :type onset: str
    :param resolution: an ISO8601 string representing the age of resolution, optional
    :type resolution: str
    """
    def __init__(self, hpo_id, label, observed=True, measured=True, onset=Constants.NOT_PROVIDED, onset_term=None, resolution=None):
        if hpo_id is None or len(hpo_id) == 0 or not hpo_id.startswith("HP"):
            raise ValueError(f"invalid id argument: '{hpo_id}'")
        if label is None or len(label) == 0:
            raise ValueError(f"invalid label argument: '{label}'")
        self._id = hpo_id
        self._label = label
        self._observed = observed
        self._measured = measured
        if onset is None:
            self._onset = Constants.NOT_PROVIDED
        else:
            self._onset = onset
        self._onset_term = onset_term
        if resolution is None:
            self._resolution = Constants.NOT_PROVIDED
        else:
            self._resolution = resolution

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other._id and self._label == other._label and self._measured == other._measured and self._onset == other._onset and self._resolution == other._resolution
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self._id, self._label, self._observed, self._measured, self._onset, self._resolution))

    @property
    def id(self):
        """
        :returns: The HPO identifier, e.g., HP:0001166
        :rtype: str
        """
        return self._id

    @property
    def label(self):
        """
        :returns: The HPO label, e.g., Arachnodactyly
        :rtype: str
        """
        return self._label

    @property
    def observed(self):
        return self._observed

    @property
    def measured(self):
        """
        :returns: True iff a measurement to assess this abnormality (HpTerm) was performed
        :rtype: bool
        """
        return self._measured

    @property
    def onset(self):
        """
        :returns: iso8601 string representing the age this abnormality first was observed
        :rtype: str, optional
        """
        return self._onset

    def set_onset(self, onset):
        self._onset = onset

    @property
    def onset_term(self):
        return self._onset_term

    @property
    def resolution(self):
        """
        :returns: iso8601 string representing the age this abnormality resolved
        :rtype: str, optional
        """
        return self._resolution

    @property
    def display_value(self):
        """
        :returns: One of three strings describing the status of the term: "not measured", "excluded", or "observed"
        :rtype: str
        """
        if not self._measured:
            return "not measured"
        if not self._observed:
            return "excluded"
        else:
            return "observed"

    @property
    def hpo_term_and_id(self):
        """
        :returns: A string such as Arachnodactyly (HP:0001166) for display
        :rtype: str
        """
        return f"{self._label} ({self._id})"

    def __str__(self) -> str:
        if not self._measured:
            return f"not measured: {self._label} ({self._id})"
        elif not self._observed:
            return f"excluded: {self._label} ({self._id})"
        else:
            return f"{self._label} ({self._id})"

    def to_string(self):
        return self.__str__()

    def excluded(self):
        """
        Sets the current term to excluded (i.e., the abnormality was sought but explicitly ruled out clinically)
        """
        self._observed = False

    def to_ga4gh_phenotypic_feature(self):
        """
        :returns: A GA4GH PhenotypcFeature corresponding to this HpTerm
        :rtype: phenopackets.PhenotypicFeature
        """
        pf = PPKt.PhenotypicFeature()
        pf.type.id = self._id
        pf.type.label = self._label
        if not self._observed:
            pf.excluded = True
        if self._onset != Constants.NOT_PROVIDED:
            pf.onset.age.iso8601duration = self._onset
        elif self.onset_term is not None:
            oclass = PPKt.OntologyClass()
            oclass.id = self._onset_term[1]
            oclass.label = self._onset_term[0]
            pf.onset.ontology_class.CopyFrom(oclass)
        if self._resolution != Constants.NOT_PROVIDED:
            pf.resolution.age.iso8601duration = self._resolution
        return pf


    @staticmethod
    def term_list_to_dataframe(hpo_list):
        if not isinstance(hpo_list, list):
            raise ValueError(f"hpo_list argument must be a list but was {type(hpo_list)}")
        if len(hpo_list) > 0:
            hpo1 = hpo_list[0]
            if not isinstance(hpo1, HpTerm):
                raise ValueError(f"hpo_list argument must consist of HpTerm objects but had {type(hpo1)}")
        if len(hpo_list) == 0:
            return pd.DataFrame(columns=['Col1', 'Col2', 'Col3'])
        items = []
        for hp in hpo_list:
            d = { "id": hp.id, "label": hp.label, "observed":hp.observed, "measured": hp.measured }
            items.append(d)
        return pd.DataFrame(items)

    @staticmethod
    def from_hpo_tk_term(hpotk_term:hpotk.Term):
        """Create a pyphetools HpTerm object from an hpo-toolkit Term object

        :param hpotk_term: A term from the HPO toolkit
        :type hpotk_term: hpotk.Term
        :returns: The corresponding HpTerm object
        :rtype: HpTerm
        """
        hpo_id = hpotk_term.identifier.value
        hpo_label = hpotk_term.name
        return HpTerm(hpo_id=hpo_id, label=hpo_label)


class HpTermBuilder:

    def __init__(self, hpo_id:str, hpo_label:str):
        if not hpo_id.startswith("HP:"):
            raise ValueError(f"Malformed HPO id {hpo_id}")
        if not len(hpo_id) == 10:
            length = len(hpo_id)
            raise ValueError(f"Malformed HPO id with length {len(hpo_id)}: {hpo_id}")
        self._hpo_id = hpo_id
        if hpo_label is None or len(hpo_label) < 3:
            raise ValueError(f"Malformed HPO label \"{hpo_label}\"")
        self._hpo_label = hpo_label
        self._observed=True
        self._measured=True
        self._onset=None
        self._onsetTerm=None

    def excluded(self):
        self._observed = False
        return self

    def not_measured(self):
        self._measured = False
        return self

    def iso8601_onset(self, onset):
        self._onset = onset
        return self

    def embryonal_onset(self):
        """Onset of disease at up to 8 weeks following fertilization (corresponding to 10 weeks of gestation).
        """
        self._onsetTerm = ["Embryonal onset", "HP:0011460"]
        return self

    def fetal_onset(self):
        """Onset prior to birth but after 8 weeks of embryonic development (corresponding to a gestational age of 10 weeks).
        """
        self._onsetTerm = ["Fetal onset", "HP:0011461"]
        return self

    def second_trimester_onset(self):
        """second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive)
        """
        self._onsetTerm = ["Second trimester onset", "HP:0034198"]
        return self

    def late_first_trimester_onset(self):
        """late first trimester during the early fetal period, which is defined as 11 0/7 to 13 6/7 weeks of gestation (inclusive).
        """
        self._onsetTerm = ["Late first trimester onset", "HP:0034199"]
        return self

    def third_trimester_onset(self):
        """third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
        """
        self._onsetTerm = ["Third trimester onset", "HP:0034197"]
        return self

    def antenatal_onset(self):
        """onset prior to birth
        """
        self._onsetTerm = ["Antenatal onset", "HP:0030674"]
        return self

    def congenital_onset(self):
        """A phenotypic abnormality that is present at birth.
        """
        self._onsetTerm = ["Congenital onset", "HP:0003577"]
        return self

    def neonatal_onset(self):
        """Onset of signs or symptoms of disease within the first 28 days of life.
        """
        self._onsetTerm = ["Neonatal onset", "HP:0003623"]
        return self


    def infantile_onset(self):
        """Onset of signs or symptoms of disease between 28 days to one year of life.
        """
        self._onsetTerm = ["Infantile onset", "HP:0003593"]
        return self

    def childhood_onset(self):
        """Onset of disease at the age of between 1 and 5 years.
        """
        self._onsetTerm = ["Childhood onset", "HP:0011463"]
        return self

    def juvenile_onset(self):
        """Onset of signs or symptoms of disease between the age of 5 and 15 years.
        """
        self._onsetTerm = ["Juvenile onset", "HP:0003621"]
        return self

    def young_adult_onset(self):
        """Onset of disease at the age of between 16 and 40 years.
        """
        self._onsetTerm = ["Young adult onset", "HP:0011462"]
        return self

    def middle_age_onset(self):
        """onset of symptoms at the age of 40 to 60 years.
        """
        self._onsetTerm = ["Middle age onset", "HP:0003596"]
        return self

    def late_onset(self):
        """Onset of symptoms after the age of 60 years.
        """
        self._onsetTerm = ["Late onset", "HP:0003584"]
        return self

    def build(self) -> HpTerm:
        if self._onset is not None and self._onsetTerm is not None:
            raise ValueError("Both onset and onsetTerm were set but only a maximum of one of them may be not None")
        return HpTerm(hpo_id=self._hpo_id,
                    label=self._hpo_label,
                    observed=self._observed,
                    measured=self._measured,
                    onset=self._onset,
                    onset_term=self._onsetTerm)


