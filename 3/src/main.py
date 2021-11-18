"""MAIN"""
from pylatex import (Document, NoEscape, Package, Alignat)
from more_itertools import pairwise
import pandas as pd
import numpy as np
from bunch import Bunch

def print_dict_table(doc, dict_):
    """dictionary as latex table to pylatex.Document"""
    pd_df = pd.DataFrame(dict_)
    mcf = '|'.join('c' * len(dict_.keys()))
    doc.append(NoEscape(pd_df.to_latex(index=False, escape=False, column_format=mcf)))


def print_central_moment(doc, grouped, nth):
    """prints nth central moment to pylatex.Document"""
    sum_ = np.sum(grouped.freq * (grouped.ranges_m - grouped.sample_mean)**nth)
    res = 1 / grouped.sample_size * sum_

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f"""\\\\ \\hat{{\\mu}}_3
            = \\frac 1 n \\sum\\limits_{{j = 1}}^L {{n_j (x_j - {grouped.sample_mean_sym})^{nth}}}
            = \\frac 1 {{ {grouped.sample_size} }} * ({sum_:.2f})
            = {res:.2f}
        """)


def np_map(func, arr):
    """same as map but returns np.array"""
    return np.array(list(map(func, arr)))


def latex():
    """Lr3"""
    freq = [3, 1, 5, 9, 9, 3]
    bin_edges = np.linspace(5.4, 11.4, 7)
    sample_mean = 8.87
    var = 1.9

    sample_mean_sym = '\\overline {{ x_{{b}} }}'

    ranges = list(pairwise(bin_edges))
    grouped = {
        'bin_edges'       : bin_edges,
        'freq'            : freq,
        'sample_mean'     : sample_mean,
        'var'             : var,
        'sample_size'     : np.sum(freq),
        'ranges'          : ranges,
        'ranges_m'        : np_map(
            lambda p: (p[0] + p[1]) / 2,
            ranges
        ),
        'sample_mean_sym' : sample_mean_sym
    }

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('booktabs'))# for print_dict_table
    print_dict_table(doc, {
        'range' : ranges,
        'freq'  : freq
    })


    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f'{sample_mean_sym} = {sample_mean:.2f}')
        agn.append(f';~ D = {var:.2f}')

    for i in [3, 4]:
        print_central_moment(doc, Bunch(grouped), i)

    doc.generate_pdf('full', clean_tex=False)
latex()
