from enum import Enum
from .hp_term import HpTerm

class Moi(Enum):
    AD="Autosomal dominant inheritance"
    AR="Autosomal recessive inheritance"
    XLI="X-linked inheritance"
    XLR="X-linked recessive inheritance"
    XLD="X-linked dominant inheritance"
    MITO="Mitochondrial inheritance"
    YLI="Y-linked inheritance"


    def to_HPO(self):
        if self == Moi.AD:
            return HpTerm(hpo_id="HP:0000006", label="Autosomal dominant inheritance")
        elif self == Moi.AR:
            return HpTerm(hpo_id="HP:0000007", label="Autosomal recessive inheritance")
        elif self == Moi.XLI:
            return HpTerm(hpo_id="HP:0001417", label="X-linked inheritance")
        elif self == Moi.XLR:
            return HpTerm(hpo_id="HP:0001419", label="X-linked recessive inheritance")
        elif self == Moi.XLD:
            return HpTerm(hpo_id="HP:0001423", label="X-linked dominant inheritance")
        elif self == Moi.MITO:
            return HpTerm(hpo_id="HP:0001427", label="Mitochondrial inheritance")
        elif self == Moi.YLI:
            return HpTerm(hpo_id="HP:0001450", label="Y-linked inheritance")
        
        else:
            raise ValueError(f"Unrecognized Moi enum (should never happen)")
