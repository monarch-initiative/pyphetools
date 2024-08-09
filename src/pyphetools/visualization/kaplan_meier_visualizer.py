import typing
import hpotk
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
            ## check for target HPO
            if spat.contains_observed_term_id(target_tid):
                observed_term = spat.get_observed_term_by_id(target_tid)
                print("found " + target_tid)
            else:
                observed_term = None
            if spat.contains_excluded_term_id(target_tid):
                excluded_term = spat.get_excluded_term_by_id(target_tid)
            else:
                excluded_term = None
            ## If we do not have a last date, we cannot include this in the KM analysis.
            ## We can tak the last date from the last_observed or from the data of the feature if it was present
            if years_at_last_exam is None and observed_term is None:
                print(f"[WARN] skipping {spat.get_phenopacket_id()} because we could not find last age/event age")
            if observed_term is not None:
                event_age = observed_term.onset
                event_years = SimplePatient.age_in_years(iso_age=event_age)
                print("event years", event_years)
            else:
                event_years = None
            if event_years is not None:
                time_in_years.append(event_years)
                event.append(1)
                n_observed += 1
            elif excluded_term is not None and years_at_last_exam is not None:
                time_in_years.append(years_at_last_exam)
                event.append(0)
                n_excluded += 1
            else:
                print(f"[WARN] skipping {spat.get_phenopacket_id()} because we could not find last age/event age (2)")
                n_invalid += 1
        print(f"observed events {n_observed}, right-censored cases {n_excluded}, invalid {n_invalid}")
        self._T = time_in_years
        self._E = event

        
    def get_time_and_event(self):
        return self._T, self._E