from collections import defaultdict
import phenopackets as PPKt
import typing


from ..creation.constants import Constants
from ..creation import Individual, HpTerm, MetaData
from .simple_patient import SimplePatient
from .html_table_generator import HtmlTableGenerator
from ..pp.v202 import display_time_element, time_element_to_days
from ..pp.v202 import TimeElement as TimeElement202


class Age2Day:
    """
    Convenience function to help sort ages but converting ISO8601 strings into the number of days

        sorted_age = sorted(l, key=lambda x: x.days)

    following this, retrieve the original string as x.key
    """
    def __init__(self, age, days) -> None:
        self.key = age
        self.days = days


class IndividualTable:

    """
    This class creates a table with a summary of  data in a cohort of individuals
    Create Individual objects and transform them into phenopackets, or import GA4GH phenopackets and display them.

        from IPython.display import HTML, display
        phenopackets = [i.to_ga4gh_phenopacket(metadata=metadata) for i in individuals]
        table = PhenopacketTable.from_phenopackets(phenopacket_list=phenopackets)
        display(HTML(table.to_html()))

    Alternatively,

        table = PhenopacketTable.from_individuals(individual_list=individuals, metadata=metadata)
        display(HTML(table.to_html()))
    """
    def __init__(self,  
                individual_list: typing.List[Individual],
                metadata: MetaData=None) -> None:
        """
        :param individual_list: List of Indidivual objects to be displayed
        :type individual_list: List[Individual]
        :param metadata: metadata about the individuals
        :type metadata: MetaData
        """
        self._spat_list = []
        pmid_count_d = defaultdict(int)
        no_pmid_found = 0
        pmid_found = 0
        for individual in individual_list:
            pp = self._individual_to_phenopacket(individual, metadata)
            spat = SimplePatient(ga4gh_phenopacket=pp)
            if spat.has_pmid():
                pmid_count_d[spat.get_pmid()] += 1
                pmid_found += 1
            else:
                no_pmid_found += 1
            self._spat_list.append(spat)
        # Create caption
        if pmid_found == 0:
            self._caption = f"{len(individual_list)} individuals with no PMIDs (consider adding this information to the MetaData)"
        else:
            pmid_strings = []
            for k, v in pmid_count_d.items():
                pmid_strings.append(f"{k} (n={v})")
            pmid_str = "; ".join(pmid_strings)
            n_phenopackets = len(individual_list)
            if n_phenopackets == 1:
                self._caption = f"{n_phenopackets} phenopacket - {pmid_str}"
            else:
                self._caption = f"{n_phenopackets} phenopackets - {pmid_str}"


    def to_html(self) -> str:
        header_items = ["Individual", "Disease", "Genotype", "Phenotypic features"]
        rows = []
        for spat in self._spat_list:
            rows.append(self._simple_patient_to_table_row(spat))
        generator = HtmlTableGenerator(caption=self._caption, header_items=header_items, rows=rows)
        return generator.get_html()


    def _individual_to_phenopacket(self, individual, metadata) -> PPKt.Phenopacket:
        """Create a phenopacket with the information from this individual

        We try to get information about the publication from the Individual object first. If this is not
        available, we look for citation information in the metadata

        Args:
            individual (_type_): _description_
            metadata (_type_): _description_

        Raises:
            ValueError: _description_
        """
        citation = individual.get_citation()
        if citation is None:
            if  metadata is None:
                raise ValueError("No citation information available in individual and metadata is None")
            else:
                citation = metadata.get_citation()
        created_by = "pyphetools" # Note that this is only used to create a table showing variants, diagnoses, and HPOs
        # the actual created by is not needed for this, and it is user to provide this constant here rather than demand the user enter it.
        # similarly, we do not need to have the version of the HPO here.
        # Note that this does not affect the code that outputs phenopackets, which need to have the correct version of this
        mdata = MetaData(created_by=created_by)
        mdata.default_versions_with_hpo(version="n/a")
        metadata = mdata.to_ga4gh()
        #  the external reference is use to show counts of PMIDs
        extref = PPKt.ExternalReference()
        extref.id = citation.pmid
        pm = citation.pmid.replace("PMID:", "")
        extref.reference = f"https://pubmed.ncbi.nlm.nih.gov/{pm}"
        extref.description = citation.title
        metadata.external_references.append(extref)
        return individual.to_ga4gh_phenopacket(metadata=metadata)

    def _simple_patient_to_table_row(self, spat:SimplePatient) -> typing.List[str]:
        """
        private method intended to create one table row that represents one individual
        :param spat: An object that represents one individual
        :type spat: SimplePatient
        """
        row_items = []
        # Patient information
        time_element = spat.get_age()
        if time_element is None:
            age_string = None
        else:
            age_string = display_time_element(time_element=time_element)
        if age_string is None:
            pat_info = spat.get_subject_id() + " (" + spat.get_sex() +  ")"
        else:
            pat_info = spat.get_subject_id() + " (" + spat.get_sex() + "; " + age_string + ")"
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


    def get_hpo_cell(self, 
                     term_by_age_dict: typing.Dict[str, HpTerm]) -> str:
        """
        :param term_by_age_dict: A dictionary with key - ISO8601 string, value - list of HpTerm objects
        :type term_by_age_dict: Dict[str,HpTerm]
        :returns: HTML code for the HTML cell
        :rtype: str
        """
        lines = []
        age2day_list = IndividualTable.get_sorted_age2data_list(term_by_age_dict.keys())
        sorted_age = sorted(age2day_list, key=lambda x: x.days)
        for onset in sorted_age:
            hpo_list = term_by_age_dict.get(onset.key)
            hpos = "; ".join([hpo.__str__() for hpo in hpo_list])
            if onset.key.element is None:
                lines.append(hpos)
            else:
                lines.append(f"<b>{onset.key}</b>: {hpos}")
        return "<br/>".join(lines)



    @staticmethod
    def get_sorted_age2data_list(ages: typing.Set[typing.Union[str,TimeElement202]]) -> typing.List[Age2Day]:
        """
        Create a sorted list of Age2Day objects that we use to display the age in the HTML output. We show terms without age of onset before all other terms.

        :param ages: A set of ISO 8601 age strings
        :type ages: Set[str]
        :returns: A list of sorted Age2Day objects
        :rtype:  List[Age2Day]
        """
        age_to_days_dict = dict()
        for age in ages:
            if isinstance(age, str):
                days = -2
            else:
                days = time_element_to_days(time_element=age)
            age_to_days_dict[age] = days

        age2day_list = list(Age2Day(age, age_to_days_dict.get(age)) for age in ages)
        sorted_list = sorted(age2day_list, key=lambda x: x.days)
        return sorted_list
