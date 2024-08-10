import math
import abc
import re
import typing
import numpy as np

DAYS_IN_WEEK = 7
AVERAGE_DAYS_IN_MONTH = 30.437
AVERAGE_DAYS_IN_YEAR = 365.25
import phenopackets as PPKt

from ..pp.v202 import OntologyClass as OntologyClass202
from ..pp.v202 import TimeElement as TimeElement202
from ..pp.v202 import Age as Age202
from ..pp.v202 import GestationalAge as GestationalAge202
from ..pp.v202 import AgeRange as AgeRange202
from ..pp.v202 import Timestamp as Timestamp202
from ..pp.v202 import TimeInterval as TimeInterval202

from .constants import Constants

# The following terms are to simplify making HpoAge objects
HPO_ONSET_TERMS = {
    # Onset of symptoms after the age of 60 years.
    "Late onset": "HP:0003584",
    # Onset of symptoms after the age of 40 years.
    "Middle age onset": "HP:0003596",
    # Onset of symptoms after the age of 16 years.
    "Young adult onset": "HP:0011462",
    # Onset of disease at an age of greater than or equal to 25 to under 40 years.
    "Late young adult onset": "HP:0025710",
    # Onset of disease at an age of greater than or equal to 19 to under 25 years.
    "Intermediate young adult onset": "HP:0025709",
    # Onset of disease at an age of greater than or equal to 16 to under 19 years.
    "Early young adult onset": "HP:0025708",
    # Onset of disease after 16 years  .
    "Adult onset": "HP:0003581",
    #Onset of signs or symptoms of disease between the age of 5 and 15 years.
    "Juvenile onset": "HP:0003621",
    #Onset of disease at the age of between 1 and 5 years.
    "Childhood onset": "HP:0011463",
    # Onset of signs or symptoms of disease between 28 days to one year of life.
    "Infantile onset": "HP:0003593",
    # Onset of signs or symptoms of disease within the first 28 days of life.
    "Neonatal onset": "HP:0003623",
    # A phenotypic abnormality that is present at birth.
    "Congenital onset": "HP:0003577",
    #  onset prior to birth
    "Antenatal onset": "HP:0030674",
    #Onset of disease at up to 8 weeks following fertilization (corresponding to 10 weeks of gestation).
    "Embryonal onset": "HP:0011460",
    # Onset prior to birth but after 8 weeks of embryonic development (corresponding to a gestational age of 10 weeks).
    "Fetal onset": "HP:0011461",
    #late first trimester during the early fetal period, which is defined as 11 0/7 to 13 6/7 weeks of gestation (inclusive).
    "Late first trimester onset": "HP:0034199",
    # second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive)
    "Second trimester onset": "HP:0034198",
    #third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
    "Third trimester onset": "HP:0034197",
}


class AgeSorter:
    MOST_NEGATIVE_INT32 = np.iinfo(np.int32).min

    ISO8601_REGEX = r"^P(\d+Y)?(\d+M)?(\d+D)?"

    HPO_AGE_TO_DAYS = {
        "Antenatal onset": -1,
        "Embryonal onset": -7 * 40,
        "Fetal onset": -7 * 29,
        "Late first trimester onset": -7 * 29,
        "Second trimester onset": -7 * 26,
        "Third trimester onset": -7 * 22,
        "Congenital onset": 0,
        "Neonatal onset": 1,
        "Pediatrial onset": 29,
        "Infantile onset": 29,
        "Childhood onset": 365.25,
        "Juvenile onset": 5 * 365.25,
        "Adult onset": 16 * 365.25,
        "Young adult onset": 16 * 365.25,
        "Early young adult onset": 16 * 365.25,
        "Intermediate young adult onset": 19 * 365.25,
        "Late young adult onset": 25 * 365.25,
        "Middle age onset": 40 * 365.25,
        "Late onset": 60 * 365.25,
    }

    def __init__(self,
                element: typing.Union[
                    GestationalAge202, Age202, AgeRange202, OntologyClass202, Timestamp202, TimeInterval202]
        ):
        self._element = element
        if isinstance(element, GestationalAge202):
            days = 7 * element.weeks + element.days
            self._num_days = -1 * days
        elif isinstance(element, Age202):
            age_str = element.iso8601duration
            match = re.search(AgeSorter.ISO8601_REGEX, age_str)
            if match:
                years = int(match.group(1))
                months = int(match.group(2))
                days = int(match.group(3))
                self._num_days = years * 365.25 + months * 30.436875 + days
            else:
                self._num_days = 0
        elif isinstance(element, AgeRange202):
            age_str = element.start.iso8601duration
            match = re.search(AgeSorter.ISO8601_REGEX, age_str)
            if match:
                years = int(match.group(1))
                months = int(match.group(2))
                days = int(match.group(3))
                self._num_days = years * 365.25 + months * 30.436875 + days
            else:
                self._num_days = 0
        elif isinstance(element, OntologyClass202):
            if element.label not in AgeSorter.HPO_AGE_TO_DAYS:
                raise ValueError(f"Could not find HPO class for {element.label}")
            self._num_days = AgeSorter.HPO_AGE_TO_DAYS[element.label]
        elif isinstance(element, Timestamp202):
            self._num_days = AgeSorter.MOST_NEGATIVE_INT32
        elif isinstance(element, TimeInterval202):
            self._num_days = AgeSorter.MOST_NEGATIVE_INT32
        else:
            raise ValueError(f"Unknown element type: {type(element)}")

    @property
    def element(self) -> typing.Union[
                    GestationalAge202, Age202, AgeRange202, OntologyClass202, Timestamp202, TimeInterval202]:
        return self._element

    @property
    def num_days(self) -> int:
        return self._num_days

    @staticmethod
    def sort_by_age(onset_list: typing.List[TimeElement202]) -> typing.List[TimeElement202]:
        agesorter_list = [AgeSorter(x) for x in onset_list]
        sorted_list = sorted(agesorter_list, key=lambda x: x.num_days)
        sorted_time_elements = [x.element for x in sorted_list]
        return sorted_time_elements


class PyPheToolsAge(metaclass=abc.ABCMeta):
    """Class for managing the various ways we have of representing Age as either an ISI 8601 string,
    a gestational age, or an HPO onset term.
    """

    def __init__(self, age_string) -> None:
        self._age_string = age_string

    @abc.abstractmethod
    def to_ga4gh_time_element(self) -> PPKt.TimeElement:
        """
        :returns: a representation of Age formated as one of the options of GA4GH TimeElement
        :rtype: PPKt.TimeElement
        """
        pass

    @abc.abstractmethod
    def is_valid(self) -> bool:
        """
        :returns:subclasses should return True if the parse was successful, otherwise False
        :rtype: bool
        """
        pass

    @abc.abstractmethod
    def to_hpo_age(self) -> "HpoAge":
        """convert this PyPheToolsAge object to an HpoAge object.
        This is the identity function if the object already is of class HpoAge. For other classes, we choose the
        HpoAge object that is most appropriate given the ISO8601 or Gestational age. The purpose of this
        function is that for HPOA output, we need to have an HPO term to denote the age of onset frequencies

        :returns: HpoAge object representing the age
        :rtype: HpoAge
        """
        pass

    @property
    def age_string(self):
        if self.is_valid():
            return self._age_string
        else:
            return Constants.NOT_PROVIDED

    @staticmethod
    def get_age_pp201(age_string: str) -> typing.Optional[TimeElement202]:
        """
        Encode the age string as a TimeElement if possible
        """
        if age_string is None or len(age_string) == 0:
            return None
        if isinstance(age_string, float) and math.isnan(age_string):
            return None  # sometimes pandas returns an empty cell as a float NaN
        if age_string.startswith("P"):
            return TimeElement202(Age202(age_string))
        elif age_string in HPO_ONSET_TERMS:
            hpo_id = HPO_ONSET_TERMS.get(age_string)
            onsetClz = OntologyClass202(id=hpo_id, label=age_string)
            return TimeElement202(onsetClz)
        elif GestationalAge.is_gestational_age(age_string):
            ga = GestationalAge(age_string)
            ga202 = GestationalAge202(weeks=ga.weeks, days=ga.days)
            return TimeElement202(ga202)
        else:
            # only warn if the user did not enter na=not available
            if age_string != 'na':
                raise ValueError(f"Could not parse \"{age_string}\" as age.")
            return None

    """
    @staticmethod
    def get_age(age_string) -> "PyPheToolsAge":
    Return an appropriate subclass of PyPheToolsAge or None
        - if starts with P interpret as an ISO 8601 age string
        - if starts with HP interpret as an HPO Onset term
        - if is a string such as 34+2 interpret as a gestation age
        - If we cannot parse, return a NoneAge obejct, a signal that no age is available
        :returns:PyPheToolsAge object (one of the subclasses)
        :rtype: PyPheToolsAge
        
        if age_string is None:
            return NoneAge("na")
        if isinstance(age_string, float) and math.isnan(age_string):
            return NoneAge("na") # sometimes pandas returns an empty cell as a float NaN
        if len(age_string) == 0:
            return NoneAge("na")
        elif age_string.startswith("P"):
            return IsoAge.from_iso8601(age_string)
        elif age_string in HPO_ONSET_TERMS:
            return HpoAge(hpo_onset_label=age_string)
        elif GestationalAge.is_gestational_age(age_string):
            return GestationalAge(age_string)
        else:
            # only warn if the user did not enter na=not available
            if age_string != 'na':
                raise ValueError(f"Could not parse \"{age_string}\" as age.")
            return NoneAge(age_string=age_string)
    """

    @staticmethod
    def age_key_to_ga4gh(age_string):
        """
        Transform an age key such as either an iso8601 string (e.g. P41Y) or an HPO Onset label (e.g., Congenital onset) into a TimeElement
        The age keys are used in the Excel template files. Currently, only iso8601 and HPO Onset are supported.
        """
        if not isinstance(age_string, str):
            raise ValueError(f"age_string argument {age_string} must be a string but was {type(age_string)}")

        age_obj = PyPheToolsAge.get_age(age_string=age_string)
        if not age_obj.is_valid():
            raise ValueError(f"Could not parse age key \"{age_string}\"")
        return age_obj.to_ga4gh_time_element()


class IsoAge(PyPheToolsAge):
    """Class to record and sort ages formated according to iso8601
    """

    def __init__(self, age_string: str, y=None, m=None, w=None, d=None):
        super().__init__(age_string)
        total_days = 0
        if y is None:
            years = 0
        else:
            years = int(y)
            total_days += AVERAGE_DAYS_IN_YEAR * y
        if m is None:
            months = 0
        else:
            months = int(m)
            total_days += AVERAGE_DAYS_IN_MONTH * m
        if w is not None:
            extradays = DAYS_IN_WEEK * int(w)
            total_days += DAYS_IN_WEEK * w
        else:
            extradays = 0
        if d is None:
            days = 0 + extradays
        else:
            days = int(d) + extradays
            total_days += d
        if days > AVERAGE_DAYS_IN_MONTH:
            extra_months = math.floor(days / AVERAGE_DAYS_IN_MONTH)
            months = months + int(extra_months)
            days = days % int(
                AVERAGE_DAYS_IN_MONTH)  # modulo arithmetic, get remaining days after months are subtracted
        if months > 11:
            extra_years = months // 12
            months = months % 12
            years = years + extra_years
        self._years = years
        self._months = months
        self._days = days
        self._total_days = total_days

    def is_valid(self):
        return True

    @property
    def years(self):
        return self._years

    @property
    def months(self):
        return self._months

    @property
    def days(self):
        return self._days

    @property
    def total_days(self):
        return self._total_days

    def to_iso8601(self):
        components = ["P"]
        if self._years > 0:
            components.append(f"{self._years}Y")
        if self._months > 0:
            components.append(f"{self._months}M")
        if self._days > 0:
            components.append(f"{self._days}D")
        if len(components) == 1:
            return "P0D"  # newborn
        else:
            return "".join(components)

    def to_hpo_age(self):
        """Convert to HpoAge object
        """
        if self._years >= 60:
            return HpoAge("Late onset")
        elif self._years >= 40:
            return HpoAge("Middle age onset")
        elif self._years >= 16:
            return HpoAge("Young adult onset")
        elif self._years >= 5:
            return HpoAge("Juvenile onset")
        elif self._years >= 1:
            return HpoAge("Childhood onset")
        elif self._months >= 1:
            return HpoAge("Infantile onset")
        elif self._days >= 1:
            return HpoAge("Neonatal onset")
        elif self._days == 0:
            return HpoAge("Congenital onset")
        else:
            raise ValueError(f"[ERROR] Could not calculate HpoAge for {self.age_string}")

    def to_ga4gh_time_element(self) -> PPKt.TimeElement:
        """
        :returns: a representation of Age formated as one of the options of GA4GH TimeElement
        :rtype: PPKt.TimeElement
        """
        time_elem = PPKt.TimeElement()
        iso8601_age = self.to_iso8601()
        if iso8601_age is None:
            raise ValueError(f"iso8601 was None")
        time_elem.age.iso8601duration = iso8601_age
        return time_elem

    @staticmethod
    def from_iso8601(iso_age: str):
        """
        :returns: IsoAge object representing the years, months, and days of the Age
        :rtype: IsoAge
        """
        original_age_string = iso_age
        if not iso_age.startswith("P"):
            raise ValueError(f"Malformed isoage string {iso_age}")
        iso_age = iso_age[1:]  # remove P
        y_idx = iso_age.find("Y")
        if y_idx > 0:
            y = int(iso_age[:y_idx])
            iso_age = iso_age[(1 + y_idx):]
        else:
            y = 0
        m_idx = iso_age.find("M")
        if m_idx > 0:
            m = int(iso_age[:m_idx])
            iso_age = iso_age[(1 + m_idx):]
        else:
            m = 0
        w_idx = iso_age.find("W")
        if w_idx > 0:
            w = int(iso_age[:w_idx])
            iso_age = iso_age[(1 + w_idx):]
        else:
            w = 0
        d_idx = iso_age.find("D")
        if d_idx > 0:
            d = int(iso_age[:d_idx])
        else:
            d = 0
        return IsoAge(y=y, m=m, w=w, d=d, age_string=original_age_string)


class HpoAge(PyPheToolsAge):
    def __init__(self, hpo_onset_label) -> None:
        super().__init__(age_string=hpo_onset_label)
        if hpo_onset_label not in HPO_ONSET_TERMS:
            raise ValueError(f"Age \"{hpo_onset_label}\" is not a valid HPO Onset term")
        self._onset_label = hpo_onset_label
        self._onset_id = HPO_ONSET_TERMS.get(hpo_onset_label)

    def to_ga4gh_time_element(self) -> PPKt.TimeElement:
        """
        :returns: a representation of Age formated as an OntologyClass (HPO Onset term)
        :rtype: PPKt.TimeElement
        """
        time_elem = PPKt.TimeElement()
        clz = PPKt.OntologyClass()
        clz.id = self._onset_id
        clz.label = self._onset_label
        time_elem.ontology_class.CopyFrom(clz)
        return time_elem

    def to_hpo_age(self):
        """Return self, this is already an HpoAge object
        """
        return self

    def is_valid(self):
        return True


class GestationalAge(PyPheToolsAge):

    def __init__(self, age_string) -> None:
        super().__init__(f"age_string")
        match = re.search(r'(\d+)\+([0-6])', age_string)
        if match:
            self._weeks = match.group(1)
            self._days = match.group(2)
        else:
            raise ValueError(f"Could not extract gestation age from \"{age_string}\".")

    @property
    def weeks(self):
        return self._weeks

    @property
    def days(self):
        return self._days

    def is_valid(self):
        return True

    def to_ga4gh_time_element(self) -> PPKt.TimeElement:
        """
        :returns: a representation of Age formated as an OntologyClass (HPO Onset term)
        :rtype: PPKt.TimeElement
        """
        time_elem = PPKt.TimeElement()
        gest_age = PPKt.GestationalAge()
        gest_age.weeks = self._weeks
        gest_age.days = self._days
        time_elem.age.gestational_age.CopyFrom(gest_age)
        return time_elem

    def to_hpo_age(self):
        """Return self, this is already an HpoAge object
        """
        if self._weeks >= 28:
            # prior to birth during the third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
            return HpoAge("Third trimester onset")  # HP:0034197
        elif self._weeks >= 14:
            # prior to birth during the second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive).
            return HpoAge("Second trimester onset")  # HP:0034198
        elif self._weeks >= 11:
            # 11 0/7 to 13 6/7 weeks of gestation (inclusive).
            return HpoAge("Late first trimester onset")  #  HP:0034199
        else:
            return HpoAge("Embryonal onset")

    @staticmethod
    def is_gestational_age(age_string):
        """Gestational age should be formated as W+D, e.g. 33+2

        :returns: True if this is formated as a gestational age, false otherwise
        :rtype: bool
        """
        match = re.search(r'\d+\+[0-6]', age_string)
        if match:
            return True
        else:
            return False
