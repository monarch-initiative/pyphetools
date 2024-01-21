import math
import pandas as pd
from .hp_term import HpTerm



class Thresholder:

    def __init__(self, unit:str, hpo_term_low=None, hpo_term_high=None, hpo_term_abn=None, threshold_low=None, threshold_high=None):
        """
        if hpo_term_low is not None and not isinstance(hpo_term_low, HpTerm):
            raise ValueError(f"hpo_term_low argument must be HpTerm but was {type(hpo_term_low)}")
        if hpo_term_high is not None and not isinstance(hpo_term_high, HpTerm):
            raise ValueError(f"hpo_term_high argument must be HpTerm but was {type(hpo_term_high)}")
        if hpo_term_abn is not None and not  not isinstance(hpo_term_abn, HpTerm):
            raise ValueError(f"hpo_term_abn argument must be HpTerm but was {type(hpo_term_abn)}")
        """
        self._hpo_low = hpo_term_low
        self._hpo_high = hpo_term_high
        self._hpo_term_abn = hpo_term_abn
        # The thresholds are allowed to be None but if they are given they must be numbers
        if threshold_low is not None and not isinstance(threshold_low, int) and not isinstance(threshold_low, float):
            raise ValueError(f"threshold_low argument must be integer or float but was {threshold_low}")
        if threshold_high is not None and not isinstance(threshold_high, int) and not isinstance(threshold_high, float):
            raise ValueError(f"threshold_high argument must be integer or float but was {threshold_high}")
        if threshold_low is not None:
            self._threshold_low = float(threshold_low)
        else:
            self._threshold_low = None
        if threshold_high is not None:
            self._threshold_high = float(threshold_high)
        else:
            self._threshold_high = None



    def _value_is_high(self, value):
        if self._threshold_high is None:
            return False
        if self._hpo_high is None:
            return False
        return self._threshold_high < value

    def _value_is_low(self, value):
        if self._threshold_low is None:
            return False
        if self._hpo_low is None:
            return False
        return self._threshold_low > value

    def _value_is_normal(self, value):
        if self._threshold_high is None or self._threshold_low is None:
            return False
        if self._hpo_term_abn is None:
            return False
        return  value >= self._threshold_low and value <= self._threshold_high


    def _non_measured_term(self):
        if self._hpo_term_abn is not None:
            return HpTerm(hpo_id=self._hpo_term_abn.id, label=self._hpo_term_abn.label, measured=False)
        elif self._hpo_high is not None:
            return HpTerm(hpo_id=self._hpo_high.id, label=self._hpo_high.label, measured=False)
        elif self._hpo_low is not None:
            return HpTerm(hpo_id=self._hpo_low.id, label=self._hpo_low.label, measured=False)
        else:
            # should never happen
            raise ValueError("No HPO Term found for unmeasured")


    def map_value(self, cell_contents) -> HpTerm:
        if isinstance(cell_contents, str):
            contents = cell_contents.strip()
            if contents.lower() == "nan":
                return HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)
        elif isinstance(cell_contents, int):
            contents = cell_contents
        elif isinstance(cell_contents, float):
            if math.isnan(cell_contents):
                return HpTerm(hpo_id=self._hpo_id, label=self._hpo_label, observed=False)
            contents = cell_contents
        else:
            raise ValueError(
                f"Malformed cell contents for ThresholdedColumnMapper: {cell_contents}, type={type(cell_contents)}")
        try:
            value = float(contents)
            if self._value_is_high(value=value):
                return self._hpo_high
            elif self._value_is_low(value=value):
                return self._hpo_low
            elif self._value_is_normal(value=value):
                return HpTerm(hpo_id=self._hpo_term_abn.id, label=self._hpo_term_abn.label, observed=False)
            else:
                return self._non_measured_term()
        except Exception as exc:
            return self._non_measured_term()


    @staticmethod
    def alkaline_phophatase_blood():
        """Alkaline phosphatase in the blook circulation
        """
        high = HpTerm(hpo_id="HP:0003155",label="Elevated circulating alkaline phosphatase concentration")
        low = HpTerm(hpo_id="HP:0003282",label="Low alkaline phosphatase")
        abn =  HpTerm(hpo_id="HP:0004379",label="Abnormality of alkaline phosphatase level")
        #alkaline phosphatase concentration
        return Thresholder(hpo_term_high=high, hpo_term_abn=abn, hpo_term_low=low, threshold_low=30,                                       threshold_high=120, unit="U/L")




