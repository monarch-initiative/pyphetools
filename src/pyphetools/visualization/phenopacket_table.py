import phenopackets
from collections import defaultdict
from .simple_patient import SimplePatient


class PhenopacketTable:
    """
    This class creates a table with a summary of all phenopackets in a cohort of individuals
    It should be used with HTML, display from IPython.display 
    """
    def __init__(self, phenopacket_list) -> None:
        """
        :param phenopacket_list: List of GA4GH phenopackets to be displayed
        """
        if not isinstance(phenopacket_list, list):
            raise ValueError(f"Expecting a list but got {type(phenopacket_list)}")
        if len(phenopacket_list) == 0:
            raise ValueError("phenopacket_list was empty")
        ppkt = phenopacket_list[0]
        if str(type(ppkt)) != "<class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>":                   
            raise ValueError(f"phenopacket argument must be GA4GH Phenopacket Schema Phenopacket but was {type(ppkt)}")
        self._phenopacket_list = phenopacket_list
    
    def _phenopacket_to_table_row(self, spat):
        """
        private method intended to create one table row that represents one individual
        :param spat: An object that represents one individual
        :type spat: SimplePatient
        """
        row_items = []
        row_items.append('<tr>')
        # Patient information
        pat_info = spat.get_subject_id() + " (" + spat.get_sex() + "; " + spat.get_age() + ")"
        row_items.append('<td>' + pat_info + '</ts>')
        row_items.append('<td>' + spat.get_disease() + '</ts>')
        # Variant information    
        var_list = spat.get_variant_list()
        if len(var_list) == 0:
            row_items.append('<td>' + "n/a" + '</td>')
        elif len(var_list) == 1:
            var = var_list[0]
            row_items.append('<td>' + var.get_display() + '</td>')
        else:
            cell_items = []
            cell_items.append("<ul>")
            for var in var_list:
                cell_items.append("<li>" + var.get_display() + "</li>")
            cell_items.append("</ul>")
            row_items.append('<td>' + " ".join(cell_items) + '</td>')
        # HPO information    
        hpo_items = []
        for k, v in spat.get_observed_hpo_d().items():
            hpo_items.append(f"{v.hpo_term_and_id}")
        row_items.append('<td class="table-data">' + "; ".join(hpo_items) + '</td>')
        row_items.append('</tr>')
        return "\n".join(row_items)
        
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
            capt = f"{len(ppack_list)} phenopackets - {pmid_str}"
        table_items = []
        table_items.append('<table style="border: 2px solid black;">\n')
        table_items.append(f'<caption>{capt}</caption>\n')
        table_items.append("""<tr>
            <th>Individual</th>
            <th>Disease</th>
            <th>Genotype</th>
            <th>Phenotypic features</th>
        </tr>
        """)
        for spat in spat_list:
            table_items.append(self._phenopacket_to_table_row(spat))
        table_items.append('</table>\n') # close table content
        return "\n".join(table_items)
        
        