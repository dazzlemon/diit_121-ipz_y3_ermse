from pylatex import Document, Section, Subsection, Alignat, Figure, NoEscape, LongTable, Command, Table, Package
from more_itertools import ichunked, pairwise
import pandas as pd
import numpy as np
import matplotlib
from plots import plot

def print_dict_table(doc, dict_):
    df = pd.DataFrame(dict_)
    mcf = '|'.join('c' * len(dict_.keys()))
    doc.append(NoEscape(df.to_latex(index=False, escape=False, column_format=mcf)))

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

def float_to_str(precision):
    def fts(x):
        stripped = f"{x:{precision}}".rstrip('0')
        if stripped[-1] == '.':
            stripped += '0'
        return stripped
    return fts

def latex_solution(data, amount_bins, width, bin_edges, freq, cumfreq, smean, variance):
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('booktabs'))# for print_dict_table
    doc.packages.append(Package('float'))# correct position for plot
    
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
        'range'                        : pairwise(bin_edges),
        'frequency'                    : freq,
        'frequency density'            : map(float_to_str('.6f'), freq    / len(data)),
        'cumulative frequency'         : cumfreq.astype(np.int32),
        'cumulative frequency density' : map(float_to_str('.6f'), cumfreq / len(data)),
    })

    with doc.create(Figure(position='H')) as plot_:
        font = {'size'   : 4}
        matplotlib.rc('font', **font)
        plot(data, freq, bin_edges, width)
        plot_.add_plot(width=NoEscape(r'1\textwidth'), dpi=10000)

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f'\\overline {{ x_{{b}} }} = {smean:.2f}')# sample mean
        agn.append(f';~ D = {variance:.2f}')# variance

    doc.generate_pdf('full', clean_tex=False)