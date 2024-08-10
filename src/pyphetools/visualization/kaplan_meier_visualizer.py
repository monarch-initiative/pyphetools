import typing
import hpotk
import numpy as np
from pyphetools.visualization.simple_patient import SimplePatient



class KaplanMeierVisualizer:
    """
    Display a Kaplan Meier (survival) curve for a cohort with respect to the age of onset of a specific feature.
    For instance

        from pyphetools.visualization import KaplanMeierVisualizer, PhenopacketIngestor, SimplePatient
        from lifelines import KaplanMeierFitter
        umod_dir = "../phenopackets/" # directory containing phenopackets to plot
        ingestor = PhenopacketIngestor(indir=umod_dir)
        ppkt_list = ingestor.get_phenopacket_list()
        simple_pt_list = [SimplePatient(ppkt) for ppkt in ppkt_list]
        hpo_id = "HP:0003774" # TermId of HPO term for the KM plot
        kmv = KaplanMeierVisualizer(simple_patient_list=simple_pt_list, target_tid=stage5crd)
        T, E = kmv.get_time_and_event()
        # plot Kaplan Meier curve
        kmf = KaplanMeierFitter()
        kmf.fit(T, E, label="Age at stage 5 kidney disease")
        ax = kmf.plot_survival_function()
        ax.set_xlabel("Years");
    """
    def __init__(self, 
                 simple_patient_list: typing.List[SimplePatient], 
                 target_tid: typing.Union[str, hpotk.TermId] = None) -> None:
        """
        The goal of this class is to provide a data for a visualization as a KaplanMeier survival curve with respect to 
        the age of onset of a specific HPO term (feature of the disease).
        TODO - also add support for survival curves with GA4GH Phenopacket VitalStatus element.
        This will be performed if the target term is None
        """
        if target_tid is None:
            self._T, self._E = self._get_time_and_event_for_vital_status(simple_patient_list=simple_patient_list)
        else:
            self._T, self._E = self._get_time_and_event_for_hpo_term(target_tid=target_tid, simple_patient_list=simple_patient_list)
            
        
       


    def _get_time_and_event_for_hpo_term(self, 
                                         target_tid:str,
                                         simple_patient_list: typing.List[SimplePatient]) -> typing.Tuple[typing.List[int], typing.List[int]]:
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
        return time_in_years, event


    def _get_time_and_event_for_vital_status(self,
                                             simple_patient_list: typing.List[SimplePatient]) -> typing.Tuple[typing.List[int], typing.List[int]]:
        time_in_years = list()
        event = list()
        n_observed = 0
        n_excluded = 0
        n_invalid = 0
        for spat in simple_patient_list:
            years_at_last_exam = spat.get_age_in_years() ## float or None
            if years_at_last_exam is None:
                print(f"[WARN] skipping individual, age at last encounter not available")
                continue
            if spat.is_deceased():
                time_in_years.append(years_at_last_exam)
                event.append(1)
                n_observed += 1
            else:
                time_in_years.append(years_at_last_exam)
                event.append(0)
                n_excluded += 1
        return time_in_years, event      



        
    def get_time_and_event(self) -> typing.Tuple[typing.List[int], typing.List[int]]:
        """
        Return lists of times and event status suitable for plotting a Kaplan Meier curve
        """
        return self._T, self._E