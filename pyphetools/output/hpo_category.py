from collections import defaultdict
from hpotk.constants.hpo.organ_system import *
from hpotk.model import TermId



class HpoCategorySet:

    def __init__(self) -> None:
        self._organ_d = defaultdict(TermId)
        


    def get_default_organ_categories(self):
        organ_d = defaultdict(TermId)
        organ_d['blood'] = ABNORMALITY_OF_BLOOD_AND_BLOOD_FORMING_TISSUES
        organ_d['genitourinary']  = ABNORMALITY_OF_GENITOURINARY_SYSTEM
        organ_d['head/neck'] = ABNORMALITY_OF_HEAD_OR_NECK
        organ_d['laboratory'] = ABNORMALITY_OF_METABOLISM_OR_HOMEOSTASIS
        organ_d['prenatal'] = ABNORMALITY_OF_PRENATAL_DEVELOPMENT_OR_BIRTH
        organ_d['breast'] = ABNORMALITY_OF_THE_BREAST
        organ_d['cardiovascular'] =  ABNORMALITY_OF_THE_CARDIOVASCULAR_SYSTEM
        organ_d['digestive'] = ABNORMALITY_OF_THE_DIGESTIVE_SYSTEM
        organ_d['ear'] = ABNORMALITY_OF_THE_EAR
        organ_d['endocrine'] = ABNORMALITY_OF_THE_ENDOCRINE_SYSTEM
        organ_d['eye'] =  ABNORMALITY_OF_THE_EYE
        organ_d['immune'] =  ABNORMALITY_OF_THE_IMMUNE_SYSTEM
        organ_d['integument'] = ABNORMALITY_OF_THE_INTEGUMENT
        organ_d['limbs'] =  ABNORMALITY_OF_THE_LIMBS
        organ_d['musculoskeletal'] = ABNORMALITY_OF_THE_MUSCULOSKELETAL_SYSTEM
        organ_d['nervous_system'] = ABNORMALITY_OF_THE_NERVOUS_SYSTEM
        organ_d['respiratory'] = ABNORMALITY_OF_THE_RESPIRATORY_SYSTEM
        organ_d['thoracic'] = ABNORMALITY_OF_THE_THORACIC_CAVITY
        organ_d['voice'] = ABNORMALITY_OF_THE_VOICE
        organ_d['cellular'] = ABNORMAL_CELLULAR_PHENOTYPE
        organ_d['constitutional'] = CONSTITUTIONAL_SYMPTOM
        organ_d['growth'] = GROWTH_ABNORMALITY
        organ_d['neoplasm'] = NEOPLASM
        return organ_d