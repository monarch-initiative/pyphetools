from collections import defaultdict
import phenopackets as PPKt
from typing import Dict, List, Set
import sys

from ..creation.constants import Constants
from ..creation import Individual, HpTerm, MetaData
from .simple_patient import SimplePatient
from .html_table_generator import HtmlTableGenerator


#


class Age2Day:
    """
    Convenience function to help sort ages but converting ISO8601 strings into the number of days

        sorted_age = sorted(l, key=lambda x: x.days)

    following this, retrieve the original string as x.key
    """
    def __init__(self, age, days) -> None:
        self.key = age
        self.days = days



class PhenopacketTable:
    """
    This class creates a table with a summary of all phenopackets in a cohort of individuals
    Create Individual objects and transform them into phenopackets, or import GA4GH phenopackets and display them.

        from IPython.display import HTML, display
        phenopackets = [i.to_ga4gh_phenopacket(metadata=metadata) for i in individuals]
        table = PhenopacketTable.from_phenopackets(phenopacket_list=phenopackets)
        display(HTML(table.to_html()))

    Alternatively,

        table = PhenopacketTable.from_individuals(individual_list=individuals, metadata=metadata)
        display(HTML(table.to_html()))
    """
    def __init__(self, phenopacket_list:List[PPKt.Phenopacket]=None,
                        individual_list:List[Individual]=None,
                        metadata:MetaData=None) -> None:
        """
        :param phenopacket_list: List of GA4GH phenopackets to be displayed
        :type phenopacket_list: List[PPKt.Phenopacket]
        :param individual_list: List of Indidivual objects to be displayed
        :type individual_list: List[Individual]
        :param metadata: metadata about the individuals
        :type metadata: MetaData
        """
        if phenopacket_list is None and individual_list is not None and metadata is not None:
            self._phenopacket_list =  [i.to_ga4gh_phenopacket(metadata=metadata.to_ga4gh()) for i in individual_list]
        elif phenopacket_list is not None and individual_list is None:
            if metadata is not None:
                raise ValueError("metadata argument not needed for phenopacket list")
            self._phenopacket_list = phenopacket_list

    @staticmethod
    def from_phenopackets(phenopacket_list:List[PPKt.Phenopacket]):
        """Initialize PhenopacketTable from list of GA4GH Phenopackets

        :param phenopacket_list: list of GA4GH Phenopackets
        :type phenopacket_list: List[PPKt.Phenopacket]

        :returns: PhenopacketTable for displaying information about a cohort
        :rtype: PhenopacketTable
        """
        if not isinstance(phenopacket_list, list):
            raise ValueError(f"Expecting a list but got {type(phenopacket_list)}")
        if len(phenopacket_list) == 0:
            raise ValueError("phenopacket_list was empty")
        ppkt = phenopacket_list[0]
        if not isinstance(ppkt, PPKt.Phenopacket):
            raise ValueError(f"phenopacket_list argument must be list of Phenopacket objects but was {type(ppkt)}")
        return PhenopacketTable(phenopacket_list=phenopacket_list)

    @staticmethod
    def from_individuals(individual_list:List[Individual], metadata:MetaData):
        """Initialize PhenopacketTable from list of GA4GH Phenopackets

        :param phenopacket_list: list of GA4GH Phenopackets
        :type phenopacket_list: List[PPKt.Phenopacket]

        :returns: PhenopacketTable for displaying information about a cohort
        :rtype: PhenopacketTable
        """
        if not isinstance(individual_list, list):
            raise ValueError(f"Expecting a list but got {type(individual_list)}")
        if len(individual_list) == 0:
            raise ValueError("individual_list was empty")
        indi = individual_list[0]
        if not isinstance(indi, Individual):
            raise ValueError(f"individual_list argument must be list of Individual objects but was {type(indi)}")
        if not isinstance(metadata, MetaData):
            raise ValueError(f"metadata argument must be pyphetools MetaData object but was {type(metadata)}")
        return PhenopacketTable(individual_list=individual_list, metadata=MetaData)

    def _simple_patient_to_table_row(self, spat:SimplePatient) -> List[str]:
        """
        private method intended to create one table row that represents one individual
        :param spat: An object that represents one individual
        :type spat: SimplePatient
        """
        row_items = []
        # Patient information
        pat_info = spat.get_subject_id() + " (" + spat.get_sex() + "; " + spat.get_age() + ")"
        row_items.append( pat_info)
        row_items.append( spat.get_disease())
        # Variant information
        var_list = spat.get_variant_list()
        if len(var_list) == 0:
            row_items.append("n/a" )
        elif len(var_list) == 1:
            var = var_list[0]
            row_items.append( var.get_display() )
        else:
            cell_items = []
            cell_items.append("<ul>")
            for var in var_list:
                cell_items.append("<li>" + var.get_display() + "</li>")
            cell_items.append("</ul>")
            row_items.append( " ".join(cell_items) )
        # HPO information
        hpo_html = self.get_hpo_cell(spat.get_term_by_age_dict())
        row_items.append( hpo_html )
        return row_items


    def get_hpo_cell(self, term_by_age_dict:Dict[str,HpTerm]) -> str:
        """
        :param term_by_age_dict: A dictionary with key - ISO8601 string, value - list of HpTerm objects
        :type term_by_age_dict: Dict[str,HpTerm]
        :returns: HTML code for the HTML cell
        :rtype: str
        """
        lines = []
        age2day_list = PhenopacketTable.get_sorted_age2data_list(term_by_age_dict.keys())
        sorted_age = sorted(age2day_list, key=lambda x: x.days)
        for onset in sorted_age:
            hpo_list = term_by_age_dict.get(onset.key)
            hpos = "; ".join([hpo.__str__() for hpo in hpo_list])
            if onset.key == Constants.NOT_PROVIDED:
                lines.append(hpos)
            else:
                lines.append(f"<b>{onset.key}</b>: {hpos}")
        return "<br/>".join(lines)

    def to_html(self):
        """create an HTML table with patient ID, age, sex, genotypes, and PhenotypicFeatures
        """
        ppack_list = self._phenopacket_list
        spat_list = []
        pmid_count_d = defaultdict(int)
        no_pmid_found = 0
        pmid_found = 0
        for pp in ppack_list:
            spat = SimplePatient(ga4gh_phenopacket=pp)
            if spat.has_pmid():
                pmid_count_d[spat.get_pmid()] += 1
                pmid_found += 1
            else:
                no_pmid_found += 1
            spat_list.append(spat)
        # Create caption
        if pmid_found == 0:
            capt = f"{len(ppack_list)} phenopackets - no PMIDs (consider adding this information to the MetaData)"
        else:
            pmid_strings = []
            for k, v in pmid_count_d.items():
                pmid_strings.append(f"{k} (n={v})")
            pmid_str = "; ".join(pmid_strings)
            n_phenopackets = len(ppack_list)
            if n_phenopackets == 1:
                capt = f"{n_phenopackets} phenopacket - {pmid_str}"
            else:
                capt = f"{n_phenopackets} phenopackets - {pmid_str}"
        header_items = ["Individual", "Disease", "Genotype", "Phenotypic features"]
        rows = []
        for spat in spat_list:
            rows.append(self._simple_patient_to_table_row(spat))
        generator = HtmlTableGenerator(caption=capt, header_items=header_items, rows=rows)
        return generator.get_html()

    @staticmethod
    def iso_to_days(iso_age:str) -> int:
        """
        Transform the ISO8601 age strings (e.g., P3Y2M) into the corresponding number of days to facilitate sorting.

        Note that if age is not provided we want to sort it to the end of the list so we transform to a very high number of days.

        :param iso_age: ISO8601 age string (e.g., P3Y2M)
        :type iso_age: str
        :returns: number of days
        :rtype: int
        """
        if iso_age == Constants.NOT_PROVIDED:
            days = sys.maxsize
        elif not iso_age.startswith("P"):
            raise ValueError(f"Invlaid age string: {age}")
        else:
            days = 0
            age = iso_age[1:]
            N = len(age)
            y = age.find("Y")
            if y != -1:
                days = days + int(365.25*int(age[:y]))
                age = age[y+1:]
            m = age.find("M")
            if m != -1:
                days = days + int(30.436875*int(age[:m]))
                age = age[m+1:]
            d = age.find("D")
            if d != -1:
                days = days + int(age[:d])
        return days

    @staticmethod
    def get_sorted_age2data_list(ages:Set[str]) -> List[Age2Day]:
        """
        Create a sorted list of Age2Day objects that we use to display the age in the HTML output.

        :param ages: A set of ISO 8601 age strings
        :type ages: Set[str]
        :returns: A list of sorted Age2Day objects
        :rtype:  List[Age2Day]
        """
        age2day_list = list(Age2Day(age, PhenopacketTable.iso_to_days(age)) for age in ages)
        sorted_list = sorted(age2day_list, key=lambda x: x.days)
        return sorted_list



