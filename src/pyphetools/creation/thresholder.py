import math
import os
import pandas as pd
from .hp_term import HpTerm

current_dir = os.path.dirname(__file__)
THRESHOLDS_FILE = os.path.join(current_dir, "data", "thresholds.tsv");

class Thresholder:

    THRESHOLDER_MAP_NEEDS_INITIALIZATION = True

    THRESHOLDER_MAP = {}

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
        self._unit = unit
        if threshold_low is not None:
            self._threshold_low = float(threshold_low)
        else:
            self._threshold_low = None
        if threshold_high is not None:
            self._threshold_high = float(threshold_high)
        else:
            self._threshold_high = None


    def set_unit(self, unit) -> None:
        """
        :param unit: a user-defined unit. This can be useful, for instance, if a paper uses mg/dL instead of SI units
        :type unit: str
        """
        self._unit = unit

    def set_high_threshold(self, value):
        """Set a user-defined high threshold value. This can be useful, for instance, if a paper uses mg/dL instead of SI units
        """
        value = float(value)
        self._threshold_high = value

    def set_low_threshold(self, value):
        """Set a user-defined low threshold value. This can be useful, for instance, if a paper uses mg/dL instead of SI units
        """
        value = float(value)
        self._threshold_low = value

    def get_reference_range(self):
        return f"{self._threshold_low}-{self._threshold_high} {self._unit}"


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
    def _get_hpo_term_or_none(hpo_id, hpo_label):
        """It is OK if we do not have threshold terms for all three possible slots (Abnormal, High, Low)
        If we do not have a term, then we return None and the thresholder object will know what to do
        """
        # It is OK if there is a blank cell or a cell with na
        if hpo_id is None or hpo_label is None:
            return None
        if len(hpo_id) == 0 or len(hpo_label) == 0:
            return None
        if hpo_id == 'na' or hpo_label == 'na':
            return None
        # if the hpo_id is present, it must be well formed
        if not hpo_id.startswith('HP:') or len(hpo_id) != 10:
            raise ValueError(f"Malformed HP id: \"{hpo_id}\"")
        # we should be good to go when we get here
        return HpTerm(hpo_id=hpo_id, label=hpo_label)

    @staticmethod
    def _get_threshold_or_none(thresh):
        """the threshold cell can be empty or na -- this is OK, return None
        Otherwise return a float
        """
        if thresh is None:
            return None
        if isinstance(thresh, str) and len(thresh) == 0:
            return None
        if isinstance(thresh, float) and math.isnan(thresh):
            return None
        return float(thresh)


    @staticmethod
    def _initialize_map():
        #current_dir = os.path.dirname(__file__)
        #thresholds_file = os.path.join(current_dir, "data", "thresholds.tsv");
        df = pd.read_csv(THRESHOLDS_FILE, delimiter="\t")
        for _, row in df.iterrows():
            label = row["label"]
            hpo_abn_label  = row["hpo_abn_label"]
            hpo_abn_id  = row["hpo_abn_id"]
            hpo_low_label  = row["hpo_low_label"]
            hpo_low_id  = row["hpo_low_id"]
            hpo_high_label  = row["hpo_high_label"]
            hpo_high_id   = row["hpo_high_id"]
            unit   = row["unit"]
            low  = row["low"]
            high  = row["high"]
            # Reference = row["Reference"] -- not needed here, for human consumption only
            hp_abnormal = Thresholder._get_hpo_term_or_none(hpo_id=hpo_abn_id, hpo_label=hpo_abn_label)
            hp_low = Thresholder._get_hpo_term_or_none(hpo_id=hpo_low_id, hpo_label=hpo_low_label)
            hp_high = Thresholder._get_hpo_term_or_none(hpo_id=hpo_high_id, hpo_label=hpo_high_label)
            low_thresh = Thresholder._get_threshold_or_none(low)
            high_thresh = Thresholder._get_threshold_or_none(high)
            thresh = Thresholder(unit=unit, hpo_term_abn=hp_abnormal, hpo_term_high=hp_high, hpo_term_low=hp_low, threshold_high=high_thresh, threshold_low=low_thresh)
            Thresholder.THRESHOLDER_MAP[label] = thresh
        Thresholder.THRESHOLDER_MAP_NEEDS_INITIALIZATION = False





    @staticmethod
    def _get_thresholder(thresholder_label, unit=None, low_thresh=None, high_thresh=None):
        if Thresholder.THRESHOLDER_MAP_NEEDS_INITIALIZATION:
            Thresholder._initialize_map()
        if not thresholder_label in Thresholder.THRESHOLDER_MAP:
            raise ValueError(f"Could not find thresholder object for \"{thresholder_label}\"")
        thresh = Thresholder.THRESHOLDER_MAP.get(thresholder_label)
        if unit is not None:
            thresh.set_unit(unit)
        if low_thresh is not None:
            thresh.set_low_threshold(low_thresh)
        if high_thresh is not None:
            thresh.set_high_threshold(high_thresh)
        return thresh


    #################
    ## Static methods for commonly used lab tests.
    ## data in data/thresholds.tsv


    @staticmethod
    def alkaline_phophatase_blood(unit=None, low_thresh=None, high_thresh=None):
        """Alkaline phosphatase in the blood circulation (U/L)
        """
        return Thresholder._get_thresholder("alkaline phosphatase blood", low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def lactate_blood(unit=None, low_thresh=None, high_thresh=None):
        """Serum lactate (0.5-1 mmol/L)
        """
        return Thresholder._get_thresholder("lactate blood", low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def potassium_blood(unit=None, low_thresh=None, high_thresh=None):
        """Serum potassium 3.5 to 5.2 mEq/L (adults)
        """
        return Thresholder._get_thresholder("lactate blood", low_thresh=low_thresh, high_thresh= high_thresh)




