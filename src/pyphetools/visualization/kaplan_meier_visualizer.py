import typing
import hpotk
import numpy as np
from pyphetools.visualization.simple_patient import SimplePatient



class KaplanMeierVisualizer:

    def __init__(self, 
                 simple_patient_list: typing.List[SimplePatient], 
                 target_tid: typing.Union[str, hpotk.TermId]=None) -> None:
        """
        The goal of this class is to provide a data for a visualization as a KaplanMeier survival curve with respect to 
        the age of onset of a specific HPO term (feature of the disease).
        TODO - also add support for survival curves with GA4GH Phenopacket VitalStatus element.
        This will be performed if the target term is None
        """
        if target_tid is None:
            raise ValueError("VitalStatus based KM curve not implemented yet")
        time_in_years = list()
        event = list()
        n_observed = 0
        n_excluded = 0
        n_invalid = 0
        for spat in simple_patient_list:
            years_at_last_exam = spat.get_age_in_years() ## float or None
            if spat.contains_observed_term_id(target_tid) and spat.contains_excluded_term_id(target_tid):
                raise ValueError(f"{spat.pat_id} listed as both observed/excluded for {target_tid}")
            if spat.contains_observed_term_id(target_tid):
                observed_term = spat.get_observed_term_by_id(target_tid)
                event_age = observed_term.onset
                event_years = SimplePatient.age_in_years(time_elem=event_age)
                if event_years is None or np.isnan(event_years):
                    print(f"[WARN] could not find age at event for {spat.get_phenopacket_id()} (Omitting)")
                    continue
                time_in_years.append(years_at_last_exam)
                event.append(1)
                n_observed += 1
            elif spat.contains_excluded_term_id(target_tid):
                if years_at_last_exam is None:
                    print(f"[WARN] {target_tid} is excluded in {spat.get_phenopacket_id()} but we did not find a last exam age")
                    continue
                else:
                    time_in_years.append(years_at_last_exam)
                    event.append(0)
                    n_excluded += 1
            else:
                print(f"[WARN] skipping {spat.get_phenopacket_id()} because target term {target_tid} was neither observed nor excluded")
                n_invalid += 1
                continue
        print(f"observed events {n_observed}, right-censored cases {n_excluded}, invalid {n_invalid}")
        self._T = time_in_years
        self._E = event

        
    def get_time_and_event(self):
        return self._T, self._E