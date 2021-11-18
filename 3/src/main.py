"""MAIN"""
from pylatex import (Document, NoEscape, Package, Alignat)
from more_itertools import pairwise
import pandas as pd
import numpy as np

def print_dict_table(doc, dict_):
    """dictionary as latex table to pylatex.Document"""
    pd_df = pd.DataFrame(dict_)
    mcf = '|'.join('c' * len(dict_.keys()))
    doc.append(NoEscape(pd_df.to_latex(index=False, escape=False, column_format=mcf)))

def latex():
    """Lr3"""
    grouped = {
        'bin edges' : np.linspace(5.4, 11.4, 7),
        'freq'      : [3, 1, 5, 9, 9, 3]
    }
    sample_mean = 8.87
    variance = 1.9

    sample_size = np.sum(grouped['freq'])
    ranges = list(pairwise(grouped['bin edges']))

    ranges_m = np.array(list(map(
        lambda p: (p[0] + p[1]) / 2,
        ranges
    )))

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('booktabs'))# for print_dict_table
    print_dict_table(doc, {
        'range' : ranges,
        'freq'  : grouped['freq']
    })

    sample_mean_sym = '\\overline {{ x_{{b}} }}'

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f'{sample_mean_sym} = {sample_mean:.2f}')
        agn.append(f';~ D = {variance:.2f}')

        sum_ = np.sum(grouped['freq'] * (ranges_m - sample_mean)**3)
        res = 1 / sample_size * sum_

        agn.append(f"""\\\\ \\hat{{\\mu}}_3
            = \\frac 1 n \\sum\\limits_{{j = 1}}^L {{n_j (x_j - {sample_mean_sym})^3}}
            = \\frac 1 {{ {sample_size} }} * ({sum_:.2f})
            = {res:.2f}
        """)

    doc.generate_pdf('full', clean_tex=False)
latex()
