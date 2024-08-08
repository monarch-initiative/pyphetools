import typing
import hpotk
from pyphetools.visualization.simple_patient import SimplePatient



class KaplanMeierVisualizer:

    def __init__(self, 
                 simple_patient_list: typing.List[SimplePatient], 
                 target_term: typing.Union[str, hpotk.TermId]=None) -> None:
        """
        The goal of this class is to provide a visualization as a KaplanMeier survival curve with respect to 
        the age of onset of a specific HPO term (feature of the disease).
        TODO - also add support for survival curves with GA4GH Phenopacket VitalStatus element.
        This will be performed if the target term is None
        """
        if target_term is None:
            raise ValueError("VitalStatus based KM curve not implemented yet")
        
        pass