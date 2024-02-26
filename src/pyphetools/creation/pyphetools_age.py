import math
import abc
import regex
from typing import Optional, Union
DAYS_IN_WEEK = 7
AVERAGE_DAYS_IN_MONTH = 30.437
AVERAGE_DAYS_IN_YEAR = 365.25
import phenopackets as PPKt

from .constants import Constants
from .hp_term import HpTerm


HPO_ONSET_TERMS = {
    # Onset of symptoms after the age of 60 years.
    "Late onset": HpTerm(hpo_id="HP:0003584", label="Late onset"),
    "Middle age onset": HpTerm(hpo_id="HP:0003596",label="Middle age onset"),
    "Young adult onset": HpTerm(hpo_id="HP:0011462", label="Young adult onset"),
    # Onset of disease after 16 years  .
    "Adult onset":  HpTerm(hpo_id="HP:0003581", label="Adult onset"),
    #Onset of signs or symptoms of disease between the age of 5 and 15 years.
    "Juvenile onset": HpTerm(hpo_id="HP:0003621", label="Juvenile onset"),
    #Onset of disease at the age of between 1 and 5 years.
    "Childhood onset": HpTerm(hpo_id="HP:0011463", label="Childhood onset"),
    # Onset of signs or symptoms of disease between 28 days to one year of life.
    "Infantile onset": HpTerm(hpo_id="HP:0003593", label="Infantile onset"),
    # Onset of signs or symptoms of disease within the first 28 days of life.
    "Neonatal onset": HpTerm(hpo_id="HP:0003623", label="Neonatal onset"),
    # A phenotypic abnormality that is present at birth.
    "Congenital onset": HpTerm(hpo_id="HP:0003577", label="Congenital onset"),
    #  onset prior to birth
    "Antenatal onset": HpTerm(hpo_id="HP:0030674", label="Antenatal onset"),
    #Onset of disease at up to 8 weeks following fertilization (corresponding to 10 weeks of gestation).
    "Embryonal onset": HpTerm(hpo_id="HP:0011460", label="Embryonal onset"),
    # Onset prior to birth but after 8 weeks of embryonic development (corresponding to a gestational age of 10 weeks).
    "Fetal onset": HpTerm(hpo_id="HP:0011461", label="Fetal onset"),
    #late first trimester during the early fetal period, which is defined as 11 0/7 to 13 6/7 weeks of gestation (inclusive).
    "Late first trimester onset": HpTerm(hpo_id="HP:0034199", label="Late first trimester onset"),
    # second trimester, which comprises the range of gestational ages from 14 0/7 weeks to 27 6/7 (inclusive)
    "Second trimester onset": HpTerm(hpo_id="HP:0034198", label="Second trimester onset"),
    #third trimester, which is defined as 28 weeks and zero days (28+0) of gestation and beyond.
    "Third trimester onset":  HpTerm(hpo_id="HP:0034197", label="Third trimester onset"),
}

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

    @property
    def age_string(self):
        return self._age_string

    @staticmethod
    def get_age(age_string):
        """Return an appropriate subclass of PyPheToolsAge or None
        - if starts with P interpret as an ISO 8601 age string
        - if starts with HP interpret as an HPO Onset term
        - if is a string such as 34+2 interpret as a gestation age
        :returns:PyPheToolsAge obejct (one of the subclasses) or None
        :rtype: Optional[PyPheToolsAge]
        """
        if age_string.startswith("P"):
            return IsoAge.from_iso8601(age_string)
        elif age_string in HPO_ONSET_TERMS:
            return HpoAge(age_string=age_string)
        elif GestationalAge.is_gestational_age(age_string):
            return GestationalAge(age_string)
        else:
            # only warn if the user did not enter na=not available
            if age_string != 'na':
                print(f"[WARNING] Could not parse {age_string} as age.")
            return Constants.NOT_PROVIDED

    @staticmethod
    def onset_to_hpo_term(onset_string:str) ->Optional[HpTerm]:
        """
        try to retrieve an HPO term that represents the age of onset. This can be either an HPO term such as Antenatal onset
        or an iso8601 string. If nothing can be found (e.g., for "na"), return None
        """
        if onset_string is None or onset_string.lower() == "na":
            return None
        iso_age = IsoAge.from_iso8601(onset_string)
        if iso_age.years >= 60:
            return HPO_ONSET_TERMS.get("Late onset")
        elif iso_age.years >= 40:
            return  HPO_ONSET_TERMS.get("Middle age onset")
        elif iso_age.years >= 16:
            return  HPO_ONSET_TERMS.get("Young adult onset")
        elif iso_age.years >= 5:
            return HPO_ONSET_TERMS.get("Juvenile onset")
        elif iso_age.years >= 1:
            return HPO_ONSET_TERMS.get("Childhood onset")
        elif iso_age.months >= 1:
            return HPO_ONSET_TERMS.get("Infantile onset")
        elif iso_age.days >= 1:
            return HPO_ONSET_TERMS.get("Neonatal onset")
        elif iso_age.days == 0:
            return HPO_ONSET_TERMS.get("Congenital onset")
        # if we get here, we could not find anything. This may be an error, because according to our template,
        # the user must enter an iso8601 string or an HPO label
        raise ValueError(f"Could not identify HPO onset term for {onset_string}")

    @staticmethod
    def to_hpo_onset_term(onset:Union['PyPheToolsAge', str]):
        if isinstance(onset, str):
            if onset in HPO_ONSET_TERMS:
                return HPO_ONSET_TERMS.get(onset)
            elif onset.startswith("P"):
                iso_age = IsoAge.from_iso8601(onset)
                return PyPheToolsAge.onset_to_hpo_term(iso_age)
            elif onset == "na" or onset == Constants.NOT_PROVIDED:
                return None
        else:
            # it must have been a PyPheToolsAge object. Check which kind
            age_string = onset.age_string
            if age_string.startswith("P"):
                iso_age = IsoAge.from_iso8601(onset)
                return PyPheToolsAge.onset_to_hpo_term(iso_age)
            elif age_string.startswith("HP"):
                if age_string in HPO_ONSET_TERMS:
                    return HPO_ONSET_TERMS.get(age_string)
                else:
                    # should never happen
                    raise ValueError(f"Invalid age string {age_string}")
            else:
                raise ValueError(f"Gestational age not yet implemented: {age_string}")





class IsoAge(PyPheToolsAge):
    """Class to record and sort ages formated according to iso8601
    """

    def __init__(self, age_string:str, y=None, m=None, w=None, d=None):
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
            days = days % int(AVERAGE_DAYS_IN_MONTH)  # modulo arithmetic, get remaining days after months are subtracted
        if months > 11:
            extra_years = months // 12
            months = months % 12
            years = years + extra_years
        self._years = years
        self._months = months
        self._days = days
        self._total_days = total_days

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
            return "P0D" # newborn
        else:
            return "".join(components)

    def to_ga4gh_time_element(self) -> PPKt.TimeElement:
        """
        :returns: a representation of Age formated as one of the options of GA4GH TimeElement
        :rtype: PPKt.TimeElement
        """
        time_elem = PPKt.TimeElement()
        iso8601_age = self.to_iso8601()
        if iso8601_age is None:
            raise ValueError(f"iso8601 was None")
        time_elem.age.iso8601duration  = iso8601_age
        return time_elem

    @staticmethod
    def from_iso8601(iso_age:str):
        """
        :returns: IsoAge object representing the years, months, and days of the Age
        :rtype: IsoAge
        """
        original_age_string = iso_age
        if not iso_age.startswith("P"):
            raise ValueError(f"Malformed isoage string {iso_age}")
        iso_age = iso_age[1:] # remove P
        y_idx = iso_age.find("Y")
        if y_idx > 0:
            y = int(iso_age[:y_idx])
            iso_age = iso_age[(1+y_idx):]
        else:
            y = 0
        m_idx = iso_age.find("M")
        if m_idx > 0:
            m = int(iso_age[:m_idx])
            iso_age = iso_age[(1+m_idx):]
        else:
            m = 0
        w_idx = iso_age.find("W")
        if w_idx > 0:
            w = int(iso_age[:w_idx])
            iso_age = iso_age[(1+w_idx):]
        else:
            w = 0
        d_idx = iso_age.find("D")
        if d_idx > 0:
            d = int(iso_age[:d_idx])
        else:
            d = 0
        return IsoAge(y=y, m=m, w=w, d=d, age_string=original_age_string)

class HpoAge(PyPheToolsAge):
    def __init__(self, age_string) -> None:
        super().__init__(age_string)
        if age_string not in HPO_ONSET_TERMS:
            raise ValueError(f"Age \"{age_string}\" is not a valid HPO Onset term")
        self._onset_term = HPO_ONSET_TERMS.get(age_string)

    def to_ga4gh_time_element(self) -> PPKt.TimeElement:
        """
        :returns: a representation of Age formated as an OntologyClass (HPO Onset term)
        :rtype: PPKt.TimeElement
        """
        time_elem = PPKt.TimeElement()
        clz = PPKt.OntologyClass()
        clz.id = self._onset_term.id
        clz.label = self._onset_term.label
        time_elem.ontology_class.CopyFrom(clz)
        return time_elem

class GestationalAge(PyPheToolsAge):

    def __init__(self, age_string) -> None:
        super().__init__(f"age_string")
        match = regex.search(r'(\d+)\+([0-6])', age_string)
        if match:
            self._weeks = match.group(1)
            self._days = match.group(2)
        else:
            raise ValueError(f"Could not extract gestation age from \"{age_string}\".")

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

    @staticmethod
    def is_gestational_age(age_string):
        """Gestational age should be formated as W+D, e.g. 33+2

        :returns: True if this is formated as a gestational age, false otherwise
        :rtype: bool
        """
        match = regex.search(r'\d+\+[0-6]', age_string)
        if match:
            return True
        else:
            return False
