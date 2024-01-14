from typing import List



class HtmlTableGenerator:
    """
    Helper class to generator an HTML table. This class is not intended to be used by client code.

    """

    def __init__(self, caption, header_items:List[str], rows:List[List[str]]) -> None:
        self._html_rows = []
        self._n_columns = len(header_items)
        self._html_rows.append('<table style="border: 2px solid black; align: "left">')
        self._html_rows.append(f'<caption>{caption}</caption>')
        self._html_rows.append(self._format_header(header_items=header_items))
        for row in rows:
            self._html_rows.append(self._format_row(row))
        self._html_rows.append('</table>') # close table content


    def _format_header(self, header_items):
        wrapped_items = [f"<th style=\"text-align: left;font-weight: bold;\">{x}</th>" for x in header_items]
        return "<tr>" + "".join(wrapped_items) + "</tr>"

    def _format_row(self, row:List[str]):
        if len(row) != self._n_columns:
            # should never happen if we construct the tables correctly
            raise ValueError(f"All rows need to have {self._n_columns} columns")
        wrapped_items = [f"<td style=\"text-align: left;\">{x}</td>" for x in row]
        return "<tr>" + "".join(wrapped_items) + "</tr>"

    def get_html(self):
        return "\n".join(self._html_rows)


