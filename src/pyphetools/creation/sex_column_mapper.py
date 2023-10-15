import pandas as pd
from .constants import Constants


class SexColumnMapper:
    """
    Mapper for a column that indicates the sex of the individual

    :param male_symbol: the synbol for males, e.g. "M", "male", "MALE"
    :type male_symbol: str
    :param female_symbol: the synbol for females, e.g. "F", "female", "FEMALE"
    :type female_symbol: str
    :param column_name: name of the sex column in the original table
    :type column_name: str
    :param other_symbol: symbol for other sex
    :type other_symbol: str
    :param unknown_symbol: symbol for unknown sex
    :type unknown_symbol: str
    :param not_provided: symbol for cases where the sex is not indicated in the original table
    :type not_provided: str
    """


    def __init__(self, male_symbol, female_symbol, column_name, other_symbol=None, unknown_symbol=None, not_provided=False) -> None:
        """
        Constructor
        """
        self._male_symbol = male_symbol
        self._female_symbol = female_symbol
        self._other_symbol = other_symbol
        self._unknown_symbol = unknown_symbol
        if column_name is None:
            raise ValueError("Must provide non-null column_name argument")
        self._column_name = column_name
        self._not_provided = not_provided

    def map_cell(self, cell_contents) -> str:
        if self._not_provided:
            return Constants.UNKOWN_SEX_SYMBOL
        contents = cell_contents.strip()
        if contents == self._female_symbol:
            return Constants.FEMALE_SYMBOL
        elif contents == self._male_symbol:
            return Constants.MALE_SYMBOL
        elif contents == self._other_symbol:
            return Constants.OTHER_SEX_SYMBOL
        elif contents == self._unknown_symbol:
            return Constants.UNKOWN_SEX_SYMBOL
        else:
            print(f"Could not map sex symbol {contents}")
            return Constants.UNKOWN_SEX_SYMBOL

    def preview_column(self, column):
        if not isinstance(column, pd.Series):
            raise ValueError("column argument must be pandas Series, but was {type(column)}")
        dlist = []
        for index, value in column.items():
            result = self.map_cell(str(value))
            if result is None:
                dlist.append({"original column contents": value, "sex": "n/a"})
            else:
                dlist.append({"original column contents": value, "sex": result})
        return pd.DataFrame(dlist)

    def get_column_name(self):
        return self._column_name
    
    @staticmethod
    def not_provided():
        """Create an object for cases where sex is not indicated.
        """
        return SexColumnMapper(male_symbol=Constants.NOT_PROVIDED, 
                               female_symbol=Constants.NOT_PROVIDED, 
                               not_provided=True, 
                               column_name=Constants.NOT_PROVIDED)

