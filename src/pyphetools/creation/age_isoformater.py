import math
from .constants import Constants

AVERAGE_DAYS_IN_MONTH = 30.437

class AgeIsoFormater:
    """
    A helper class that formats year, month, week, days into ISO 8601 strings

    :param y: years
    :type y: Union(int,str), optional
    :param m: months
    :type m: Union(int,str), optional
    :param w: weeks
    :type w: Union(int,str), optional
    :param d: days
    :type d: Union(int,str), optional


    """

    def __init__(self, y=None, m=None, w=None, d=None):
        if y is None:
            years = 0
        else:
            years = int(y)
        if m is None:
            months = 0
        else:
            months = int(m)
        if w is not None:
            extradays = 7 * int(w)
        else:
            extradays = 0
        if d is None:
            days = 0 + extradays
        else:
            days = int(d) + extradays
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
    def to_string(y=None, m=None, w=None, d=None):
        """
        :param y: years
        :type y: Union(int,str), optional
        :param m: months
        :type m: Union(int,str), optional
        :param w: weeks
        :type w: Union(int,str), optional
        :param d: days
        :type d: Union(int,str), optional
        :returns: ISO8601 string representing age
        :rtype: str
        """
        formater = AgeIsoFormater(y=y, m=m, w=w, d=d)
        return formater.to_iso8601()


    @staticmethod
    def from_numerical_month(month):
        """
        decode entries such as 18 or 0.7 (number of months)
        """
        month = str(month)
        if month.isdigit():
            full_months = int(month)
            days = 0
        elif month.replace('.', '', 1).isdigit() and month.count('.') < 2:
            # a float such as 0.9 (months)
            months = float(month)
            avg_num_days_in_month = 30.437
            floor_months = math.floor(months)
            if floor_months == 0.0:
                days = int(months * avg_num_days_in_month)
                full_months = 0
            else:
                remainder = months - floor_months
                full_months = int(months - remainder)
                days = int(remainder * avg_num_days_in_month)
        else:
            return Constants.NOT_PROVIDED
        formater = AgeIsoFormater(m=full_months, d=days)
        return formater.to_iso8601()



