import pandas as pd
import phenopackets as PPKt
from .constants import Constants
from .pyphetools_age import HpoAge, IsoAge, NoneAge, PyPheToolsAge
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
    def __init__(self, hpo_id:str, label:str, observed:bool=True, measured:bool=True, onset=NoneAge("na"), resolution=NoneAge("na")):
        if hpo_id is None or len(hpo_id) == 0 or not hpo_id.startswith("HP"):
            raise ValueError(f"invalid id argument: '{hpo_id}'")
        if label is None or len(label) == 0:
            raise ValueError(f"invalid label argument: '{label}'")
        self._id = hpo_id
        self._label = label
        self._observed = observed
        self._measured = measured
        if not isinstance(onset, PyPheToolsAge):
            raise ValueError(f"onset argument must be PyPheToolsAge or subclass but was {type(onset)}")
        self._onset = onset
        self._resolution = resolution

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other._id and self._label == other._label and self._measured == other._measured and self._onset == other._onset and self._resolution == other._resolution
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self._id, self._label, self._observed, self._measured, self._onset, self._resolution))

    @property
    def id(self) -> str:
        """
        :returns: The HPO identifier, e.g., HP:0001166
        :rtype: str
        """
        return self._id

    @property
    def label(self) -> str:
        """
        :returns: The HPO label, e.g., Arachnodactyly
        :rtype: str
        """
        return self._label

    @property
    def observed(self) -> bool:
        """
        :returns: True if this feature was observed (i.e., present)
        :rtype: bool
        """
        return self._observed

    @property
    def measured(self) -> bool:
        """
        :returns: True iff a measurement to assess this abnormality (HpTerm) was performed
        :rtype: bool
        """
        return self._measured

    @property
    def onset(self) -> PyPheToolsAge:
        """
        :returns: A PyPheToolsAge object representing the age this abnormality first was observed
        :rtype: PyPheToolsAge
        """
        return self._onset

    def set_onset(self, onset:PyPheToolsAge) -> None:
        if not isinstance(onset, PyPheToolsAge):
            raise ValueError(f"argument of set_onset but be PyPheToolsAge but was {type(onset)}")
        self._onset = onset


    @property
    def resolution(self) -> PyPheToolsAge:
        """
        :returns: A PyPheToolsAge object representing the age this abnormality resolved
        :rtype: PyPheToolsAge
        """
        return self._resolution

    @property
    def display_value(self) -> str:
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
    def hpo_term_and_id(self) -> str:
        """
        :returns: A string such as Arachnodactyly (HP:0001166) for display
        :rtype: str
        """
        return f"{self._label} ({self._id})"

    def _term_and_id_with_onset(self) -> str:
        if self._onset is not None and self._onset.is_valid():
            return f"{self.hpo_term_and_id}: onset {self._onset.age_string}"
        else:
            return self.hpo_term_and_id

    def __str__(self) -> str:
        if not self._measured:
            return f"not measured: {self._label} ({self._id})"
        elif not self._observed:
            return f"excluded: {self._term_and_id_with_onset()}"
        else:
            return self._term_and_id_with_onset()

    def to_string(self) -> str:
        return self.__str__()

    def excluded(self) -> None:
        """
        Sets the current term to excluded (i.e., the abnormality was sought but explicitly ruled out clinically)
        """
        self._observed = False

    def to_ga4gh_phenotypic_feature(self) -> PPKt.PhenotypicFeature:
        """
        :returns: A GA4GH PhenotypcFeature corresponding to this HpTerm
        :rtype: phenopackets.PhenotypicFeature
        """
        pf = PPKt.PhenotypicFeature()
        pf.type.id = self._id
        pf.type.label = self._label
        if not self._observed:
            pf.excluded = True
        if self._onset.is_valid():
            pf.onset.CopyFrom(self._onset.to_ga4gh_time_element())
        if self._resolution.is_valid():
            pf.resolution.CopyFrom(self._resolution.to_ga4gh_time_element())
        return pf


    @staticmethod
    def term_list_to_dataframe(hpo_list) -> pd.DataFrame:
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
    def from_hpo_tk_term(hpotk_term:hpotk.Term) -> "HpTerm":
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
            raise ValueError(f"Malformed HPO id with length {len(hpo_id)}: {hpo_id}")
        self._hpo_id = hpo_id
        if hpo_label is None or len(hpo_label) < 3:
            raise ValueError(f"Malformed HPO label \"{hpo_label}\"")
        self._hpo_label = hpo_label
        self._observed = True
        self._measured = True
        self._onset = NoneAge("na")
        self._resolution = NoneAge("na")

    def excluded(self):
        self._observed = False
        return self

    def not_measured(self):
        self._measured = False
        return self

    def iso8601_onset(self, onset):
        """Set the age with an iso8601 string
        """
        if not isinstance(onset, str):
            raise ValueError(f"onset argument must be iso8601 string but was {type(onset)}")
        self._onset = IsoAge.from_iso8601(onset)
        return self

    def embryonal_onset(self):
        """Onset of disease at up to 8 weeks following fertilization (corresponding to 10 weeks of gestation).
        """
        self._onsetTerm = HpoAge("Embryonal onset") # HP:0011460
        return self

    def fetal_onset(self):
        """Onset prior to birth but after 8 weeks of embryonic development (corresponding to a gestational age of 10 weeks).
        """
        self._onset = HpoAge("Fetal onset") # HP:0011461
        return self

    def second_trimester_onset(self):
        """second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive)
        """
        self._onset = HpoAge("Second trimester onset") # HP:0034198
        return self

    def late_first_trimester_onset(self):
        """late first trimester during the early fetal period, which is defined as 11 0/7 to 13 6/7 weeks of gestation (inclusive).
        """
        self._onset = HpoAge("Late first trimester onset") # HP:0034199
        return self

    def third_trimester_onset(self):
        """third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
        """
        self._onset = HpoAge("Third trimester onset") # HP:0034197
        return self

    def antenatal_onset(self):
        """onset prior to birth
        """
        self._onset = HpoAge("Antenatal onset") # HP:0030674
        return self

    def congenital_onset(self):
        """A phenotypic abnormality that is present at birth.
        """
        self._onset = HpoAge("Congenital onset") # HP:0003577
        return self

    def neonatal_onset(self):
        """Onset of signs or symptoms of disease within the first 28 days of life.
        """
        self._onset = HpoAge("Neonatal onset") # HP:0003623)
        return self


    def infantile_onset(self):
        """Onset of signs or symptoms of disease between 28 days to one year of life.
        """
        self._onset = HpoAge("Infantile onset") # HP:0003593
        return self

    def childhood_onset(self):
        """Onset of disease at the age of between 1 and 5 years.
        """
        self._onset = HpoAge("Childhood onset") # HP:0011463
        return self

    def juvenile_onset(self):
        """Onset of signs or symptoms of disease between the age of 5 and 15 years.
        """
        self._onset = HpoAge("Juvenile onset") # HP:0003621
        return self

    def young_adult_onset(self):
        """Onset of disease at the age of between 16 and 40 years.
        """
        self._onset = HpoAge("Young adult onset") # HP:0011462
        return self

    def middle_age_onset(self):
        """onset of symptoms at the age of 40 to 60 years.
        """
        self._onset = HpoAge("Middle age onset") # HP:0003596
        return self

    def late_onset(self):
        """Onset of symptoms after the age of 60 years.
        """
        self._onset = HpoAge("Late onset") # HP:0003584
        return self

    def build(self) -> HpTerm:
        return HpTerm(hpo_id=self._hpo_id,
                    label=self._hpo_label,
                    observed=self._observed,
                    measured=self._measured,
                    onset=self._onset)

