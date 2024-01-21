from ..creation.hp_term import HpTerm


class SimpleAge:

    def __init__(self, age_string) -> None:
        self._age_string = age_string
        self._gestational_weeks = None
        self._gestational_days = None
        self._years = None
        self._months = None
        self._weeks = None
        self._days = None

        if age_string.startswith("P"):
            self._parse_iso8601()
        elif age_string.startswith("GA"):
            self._parse_gestational_age()
        else:
            raise ValueError(f"Malformed age string (must be iso8601 or gestational age) : {age_string}")


    def _parse_gestational_age():
        raise ValueError("not implemented yet")


    def _parse_iso8601(self):
        iso8601 = self._age_string[1:]
        self._days = 0
        if "Y" in iso8601:
            i = iso8601.index("Y")
            self._years = int(iso8601[:i])
            iso8601 = iso8601[(1+i):]
        else:
            self._years = 0
        if "M" in iso8601:
            i = iso8601.index("M")
            self._months = int(iso8601[:i])
            iso8601 = iso8601[(1+i):]
        else:
            self._months = 0
        if "W" in iso8601:
            # don't keep weeks; convert to days
            i = iso8601.index("W")
            self._days +=  7 * int(iso8601[:i])
            iso8601 = iso8601[(1+i):]
        else:
            self._weeks = 0
        if "D" in iso8601:
            i = iso8601.index("D")
            self._days += int(iso8601[:i])
        # for sorting, we will use the following expression for total days
        t = 365.25 * self._years + 30.437 * self._months + self._days
        self._total_days = int(t)


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._age_string == other._age_string
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self._age_string)

    def __str__(self) -> str:
        return self._age_string

    def get_total_days(self) -> int:
        """get total number of days of life. This simplifies sorting.
        """
        return self._total_days

    def to_hpo_onset_term(self):
        if self._years > 60:
            return HpTerm(hpo_id="HP:0003584", label="Late onset")
        if self._years >= 40:
            return HpTerm(hpo_id="HP:0003596", label="Middle age onset")
        if self._years >= 25:
            return HpTerm(hpo_id="HP:0025710", label="Late young adult onset")
        if self._years >= 19:
            return HpTerm(hpo_id="HP:0025709", label="Intermediate young adult onset")
        if self._years >= 16:
            return HpTerm(hpo_id="HP:0011462", label="Early young adult onset")
        if self._years > 5 or (self._years==5 and self._months > 0):
            return HpTerm(hpo_id="HP:0003621", label="Juvenile onset")
        if self._years >= 1:
            return HpTerm(hpo_id="HP:0011463", label="Childhood onset")
        if self._months >= 1:
            return HpTerm(hpo_id="HP:0003593", label="Infantile onset")
        if self._days > 1:
            return HpTerm(hpo_id="HP:0003623", label="Neonatal onset")
        if self._days == 0 or self._days == 1:
            return HpTerm(hpo_id="HP:0003577", label="Congenital onset")
        raise ValueError(f"Could not find onset for {self._age_string}")

