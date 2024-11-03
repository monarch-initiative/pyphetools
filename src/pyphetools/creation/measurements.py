import typing
from ..pp.v202 import Measurement as Measurement202
from ..pp.v202 import OntologyClass as OntologyClass202
from ..pp.v202 import Value as Value202
from ..pp.v202 import Quantity as Quantity202
from ..pp.v202 import ReferenceRange as ReferenceRange202


ng_per_dl = OntologyClass202(id="UCUM:ng/dL", label="nanogram per deciliter")
ng_per_ml = OntologyClass202(id="UCUM:ng/mL", label="nanogram per milliliter")
pg_per_l = OntologyClass202(id="UCUM:pg/L", label="picogram per liter")
pg_per_ml = OntologyClass202(id="UCUM:pg/mL", label="picogram per milliliter")
nmol_per_l = OntologyClass202(id="UCUM:nmol/L", label="nanomole per liter")
mmol_per_l= OntologyClass202(id="UCUM:mmol/L", label="millimole per liter")
percent = OntologyClass202(id="UCUM:%", label="percent")


class Measurements:
    """
    Convenience class with static methods to create Measurement objects for common units.
    """
    

    @staticmethod
    def _with_reference_range(assay: OntologyClass202,
                              unit: OntologyClass202,
                              value: float,
                              low: float,
                              high: float) -> Measurement202:
        refrange = ReferenceRange202(unit=unit, low=low, high=high)
        val = Value202(Quantity202(unit=unit, value=value, reference_range=refrange))
        return Measurement202(assay=assay, measurement_value=val)

    @staticmethod
    def _without_reference_range(assay: OntologyClass202,
                                unit: OntologyClass202,
                                value: float) -> Measurement202:
        val = Value202(Quantity202(unit=unit, value=value))
        return Measurement202(assay=assay, measurement_value=val)
    
    @staticmethod
    def _from_assay_and_values(assay: OntologyClass202,
                            unit: OntologyClass202,
                            value: float,
                            low: float,
                            high: float) -> Measurement202:
        if low is not None and high is not None:
            return Measurements._with_reference_range(assay=assay, unit=unit, value=value, low=low, high=high)
        else:
            return Measurements._without_reference_range(assay=assay, unit=unit, value=value)
    
    @staticmethod
    def nanogram_per_deciliter(code: str,
                       label: str,
                       concentration: float,
                       low: float = None,
                       high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=ng_per_dl, value=concentration, low=low, high=high)
        
        
    @staticmethod
    def nanogram_per_milliliter(code: str,
                       label: str,
                       concentration: float,
                       low: float = None,
                       high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=ng_per_ml, value=concentration, low=low, high=high)
       
        
    @staticmethod 
    def picogram_per_liter(code: str,
                    label: str,
                    concentration: float,
                    low: float = None,
                    high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=pg_per_l, value=concentration, low=low, high=high)
    
    @staticmethod 
    def picogram_per_milliliter(code: str,
                    label: str,
                    concentration: float,
                    low: float = None,
                    high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=pg_per_ml, value=concentration, low=low, high=high)
       
        
    @staticmethod
    def nanomole_per_liter(code: str,
                    label: str,
                    concentration: float,
                    low: float = None,
                    high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=nmol_per_l, value=concentration, low=low, high=high)
    
    @staticmethod
    def millimole_per_liter(code: str,
                    label: str,
                    concentration: float,
                    low: float = None,
                    high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=mmol_per_l, value=concentration, low=low, high=high)
    
    @staticmethod
    def percent(code: str,
                    label: str,
                    concentration: float,
                    low: float = None,
                    high: float = None) -> Measurement202:
        assay = OntologyClass202(id=code, label=label)
        return Measurements._from_assay_and_values(assay=assay, unit=percent, value=concentration, low=low, high=high)


  

        

   