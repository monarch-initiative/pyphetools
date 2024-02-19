
import math
DAYS_IN_WEEK = 7
AVERAGE_DAYS_IN_MONTH = 30.437
AVERAGE_DAYS_IN_YEAR = 365.25


class IsoAge:
    """Class to record and sort ages formated according to iso8601
    """

    def __init__(self, y=None, m=None, w=None, d=None):
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

    @staticmethod
    def from_iso8601(iso_age:str):
        """
        :returns: IsoAge object representing the years, months, and days of the Age
        :rtype: IsoAge
        """
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
        return IsoAge(y=y, m=m, w=w, d=d)

