from pylatex import Document, Section, Subsection, Alignat, Figure, NoEscape, LongTable, Command, Table, Package
from more_itertools import ichunked, pairwise
import pandas as pd

def print_dict_table(doc, dict_):
    df = pd.DataFrame(dict_)
    doc.append(NoEscape(df.to_latex(index=False, escape=False)))

def print_table(doc, data, caption, row_size=10):
    if len(data) < row_size:
        row_size = len(data)

    doc.append(caption)
    with doc.create(LongTable("l " * row_size)) as table:
        for i in ichunked(data, row_size):
            i = list(i)
            # for last row
            while len(i) < row_size:
                i.append('')
            table.add_row(i)

def latex_solution(data, amount_bins, width, bin_edges, freq):
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('booktabs'))# for print_dict_table
    
    print_table(doc, data, 'input data')
    print_table(doc, sorted(data), 'variational series')
    
    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        min_ = min(data)
        max_ = max(data)

        agn.append(f'x_{{min}} = {min_}; ~ x_{{max}} = {max_} \\\\')
        agn.append(
            f'''L = {amount_bins};
            ~ h = \\frac {{ x_{{max}} - x_{{min}} }} L
                = \\frac {{ {max_} - {min_} }} {amount_bins}
                = {width}'''
        )

    print_table(doc, bin_edges, 'bin edges')

    print_dict_table(doc, {
        'range'     : pairwise(bin_edges),
        'frequency' : freq,
    })

    doc.generate_pdf('full', clean_tex=False)