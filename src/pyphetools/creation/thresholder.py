import math
import os
import pandas as pd
from .hp_term import HpTerm
from .constants import Constants

current_dir = os.path.dirname(__file__)
THRESHOLDS_FILE = os.path.join(current_dir, "data", "thresholds.tsv");

class Thresholder:
    """A class to simplify the interpretation of thresholded values

    The class organizes the interpretation of numerical values for tests such as blood potassium. Results
    can be low, normal, or high, and there is an HPO term for each. The class also provides
    commonly used normal ranges. We note that many lab tests have different ranges for males and females or
    for adults and children. We do not attempt to model this, but instead provide ranges for adults.
    In cases where there are different ranges for males and females, we by default use the minimum and maximum
    value for each sex. It is possible to specify the range that should be used in the constructor method;
    in this case, the default values are overriden. In very complicated cases with multiple different
    normal ranges, consider using the OptionColumnMapper.
    """

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
        self._threshold_low = self._set_threshold_to_float_or_none(threshold_low)
        self._threshold_high = self._set_threshold_to_float_or_none(threshold_high)

    def _set_threshold_to_float_or_none(self, thresh):
        """in the input file, a threshold value can be set to na or n/a. If so, we set the value to None.
        Otherwise, we convert all values to floats
        """
        if thresh is not None:
            return float(thresh)
        else:
            return None


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
                return HpTerm(hpo_id=self._hpo_term_abn.id, label=self._hpo_term_abn.label, measured=False)
        elif isinstance(cell_contents, int):
            contents = cell_contents
        elif isinstance(cell_contents, float):
            if math.isnan(cell_contents):
                return HpTerm(hpo_id=self._hpo_term_abn.id, label=self._hpo_term_abn.label, measured=False)
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
        if isinstance(thresh, str):
            if len(thresh) == 0 or thresh == 'na' or thresh == "n/a":
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
            """
            # Uncomment to test whether there are format errors
            for item in [hpo_abn_label, hpo_abn_id, hpo_low_label, hpo_low_id,hpo_high_label, hpo_high_id]:
                if item.startswith(" ") or item.endswith(" "):
                    raise ValueError(f"Mqlformed HPO term: \"{item}\"")
            """
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
    def albumin_urine(unit=None, low_thresh=None, high_thresh=None):
        """Albuminuria - Urine Albumin-Creatinine Ratio (uACR)
        """
        return Thresholder._get_thresholder("albumin urine", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def ALT_blood(unit=None, low_thresh=None, high_thresh=None):
        """ALT blood
        """
        return Thresholder._get_thresholder("ALT blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def AST_blood(unit=None, low_thresh=None, high_thresh=None):
        """AST blood
        """
        return Thresholder._get_thresholder("AST blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)


    @staticmethod
    def alkaline_phophatase_blood(unit=None, low_thresh=None, high_thresh=None):
        """Alkaline phosphatase in the blood circulation (U/L)
        """
        return Thresholder._get_thresholder("alkaline phosphatase blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def ALT_blood(unit=None, low_thresh=None, high_thresh=None):
        """ALT_blood in the blood circulation (U/L)‚
        """
        return Thresholder._get_thresholder("ALT blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def AST_blood(unit=None, low_thresh=None, high_thresh=None):
        """AST_blood in the blood circulation (U/L)‚
        """
        return Thresholder._get_thresholder("AST blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def calcium_blood(unit=None, low_thresh=None, high_thresh=None):
        """Calcium in the blood circulation 8.5 to 10.2 mg/dL (2.13 to 2.55 millimol/L).
        """
        return Thresholder._get_thresholder("calcium blood",unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)


    @staticmethod
    def creatine_kinase_blood(unit=None, low_thresh=None, high_thresh=None):
        """CK females is 30 to 145 U/L; males 55 to 170 U/L
        """
        return Thresholder._get_thresholder("creatine kinase blood", unit=unit, low_thresh=low_thresh, high_thresh=high_thresh)


    @staticmethod
    def creatinine_blood(unit=None, low_thresh=None, high_thresh=None):
        """Serum crea,  0.6-1.2 mg/dL in adult males and 0.5-1.1 mg/dL in adult females
        """
        return Thresholder._get_thresholder("creatinine blood", unit=unit, low_thresh=low_thresh, high_thresh=high_thresh)


    @staticmethod
    def CRP_blood(unit=None, low_thresh=None, high_thresh=None):
        """ CRP blood
        """
        return Thresholder._get_thresholder("CRP blood", unit=unit, low_thresh=low_thresh, high_thresh=high_thresh)

    @staticmethod
    def free_fatty_acid_blood(unit=None, low_thresh=None, high_thresh=None):
        """free fatty acid
        """
        return Thresholder._get_thresholder("free fatty acid blood", unit=unit, low_thresh=low_thresh, high_thresh=high_thresh)

    @staticmethod
    def glucose_blood(unit=None, low_thresh=None, high_thresh=None):
        """fasting blood glucose; 70 mg/dL (3.9 mmol/L) and 100 mg/dL (5.6 mmol/L).
        """
        return Thresholder._get_thresholder("glucose blood", unit=unit, low_thresh=low_thresh, high_thresh=high_thresh)

    @staticmethod
    def hemoglobin_A1c(unit=None, low_thresh=None, high_thresh=None):
        """hemoglobin_A1c
        """
        return Thresholder._get_thresholder("hemoglobin A1c", unit=unit, low_thresh=low_thresh, high_thresh=high_thresh)



    @staticmethod
    def HDL_cholesterol_blood(unit=None, low_thresh=None, high_thresh=None):
        """HDL cholesterol blood
        """
        return Thresholder._get_thresholder("HDL cholesterol blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def insulin_blood(unit=None, low_thresh=None, high_thresh=None):
        """insulin blood
        """
        return Thresholder._get_thresholder("insulin blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)


    @staticmethod
    def lactate_blood(unit=None, low_thresh=None, high_thresh=None):
        """Serum lactate (0.5-1 mmol/L)
        """
        return Thresholder._get_thresholder("lactate blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def LDL_cholesterol_blood(unit=None, low_thresh=None, high_thresh=None):
        """LDL cholesterol blood
        """
        return Thresholder._get_thresholder("LDL cholesterol blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def NTproBNP_blood(unit=None, low_thresh=None, high_thresh=None):
        """NT-proBNP < 100 picograms per milliliter (pg/mL)
        """
        return Thresholder._get_thresholder("NT-proBNP blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def sodium_blood(unit=None, low_thresh=None, high_thresh=None):
        """Sodium in the blood circulation 135-145 mEq/L
        """
        return Thresholder._get_thresholder("sodium blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def potassium_blood(unit=None, low_thresh=None, high_thresh=None):
        """Serum potassium 3.5 to 5.2 mEq/L (adults)
        """
        return Thresholder._get_thresholder("potassium blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def total_cholesterol_blood(unit=None, low_thresh=None, high_thresh=None):
        """total cholesterol blood
        """
        return Thresholder._get_thresholder("total cholesterol blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)


    @staticmethod
    def triglyceride_blood(unit=None, low_thresh=None, high_thresh=None):
        """triglyceride blood
        """
        return Thresholder._get_thresholder("triglyceride blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)

    @staticmethod
    def troponin_t_blood(unit=None, low_thresh=None, high_thresh=None):
        """troponin t blood
        """
        return Thresholder._get_thresholder("troponin t blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)


    @staticmethod
    def uric_acid_blood(unit=None, low_thresh=None, high_thresh=None):
        """uric acid blood
        """
        return Thresholder._get_thresholder("uric acid blood", unit=unit, low_thresh=low_thresh, high_thresh= high_thresh)




