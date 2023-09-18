import phenopackets
from .simple_patient import SimplePatient


class PhenopacketTable:
    """
    This class creates a table with a summary of all phenopackets in a cohort of individuals
    It should be used with HTML, display from IPython.display 
    """
    def __init__(self, phenopacket_list) -> None:
        if not isinstance(phenopacket_list, list):
            raise ValueError(f"Expecting a list but got {type(phenopacket_list)}")
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
        table_items = []
        table_items.append('<table style="border: 2px solid black;">\n')
        table_items.append("""<tr>
            <th>Individual</th>
            <th>Disease</th>
            <th>Genotype</th>
            <th>Phenotypic features</th>
        </tr>
      """)
        for pp in self._phenopacket_list:
            if isinstance(pp, SimplePatient):
                spat = pp
            else:
                spat = SimplePatient(ga4gh_phenopacket=pp)
            table_items.append(self._phenopacket_to_table_row(spat))
        table_items.append('</table>\n') # close table content
        return "\n".join(table_items)
        
        