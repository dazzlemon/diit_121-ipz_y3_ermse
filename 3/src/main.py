"""MAIN"""
from pylatex import (Document, NoEscape, Package, Alignat, Figure)
from more_itertools import pairwise
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from bunch import Bunch
from math import sqrt

def print_dict_table(doc, dict_):
    """dictionary as latex table to pylatex.Document"""
    pd_df = pd.DataFrame(dict_)
    mcf = '|'.join('c' * len(dict_.keys()))
    doc.append(NoEscape(pd_df.to_latex(index=False, escape=False, column_format=mcf)))


def print_central_moment(doc, grouped, nth):
    """
    prints nth central moment to pylatex.Document
    """
    sum_, res = central_moment(grouped, nth)

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        # agn.append(f"""\\\\ \\hat{{\\mu}}_{nth}
        agn.append(f"""\\\\ \\mu_{nth}
            = \\frac 1 n \\sum\\limits_{{j = 1}}^L {{n_j (x_j - {grouped.sample_mean_sym})^{nth}}}
            = \\frac 1 {{ {grouped.sample_size} }} * ({sum_:.2f})
            = {res:.2f}
        """)


def central_moment(grouped, nth):
    """returns nth central_moment and sum needed to calculate it"""
    sum_ = np.sum(grouped.freq * (grouped.ranges_m - grouped.sample_mean)**nth)
    res = 1 / grouped.sample_size * sum_
    return sum_, res


def np_map(func, arr):
    """same as map but returns np.array"""
    return np.array(list(map(func, arr)))


def print_frac(doc, name, numerator_name, denominator_name,
    numerator, denominator, result):
    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f"""{name}
            = \\frac {{{numerator_name}}} {{{denominator_name}}}
            = \\frac {{{numerator:.2f}}} {{{denominator:.2f}}}
            = {result:.2f}
        """)


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
    doc.packages.append(Package('float'))# correct position for plot
    print_dict_table(doc, {
        'range' : ranges,
        'freq'  : freq
    })

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f'{sample_mean_sym} = {sample_mean:.2f}')
        agn.append(f'\\\\ \\mu_2 = D = {var:.2f}')

    _, mu_3 = central_moment(Bunch(grouped), 3)
    _, mu_4 = central_moment(Bunch(grouped), 4)

    print_central_moment(doc, Bunch(grouped), 3)
    print_central_moment(doc, Bunch(grouped), 4)

    assym_coef = mu_3 ** 2 / var ** 3
    excess_coef = mu_4 / var ** 2

    print_frac(doc, '\\beta_1^2', '\\mu_2^3', '\\mu_3^2', var**3, mu_3**2, assym_coef)
    print_frac(doc, '\\beta_2', '\\mu_4', '\\mu_2^2', mu_4, var**2, excess_coef)

    with doc.create(Figure(position='H')) as plot_:
        font = {'size': 4}
        matplotlib.rc('font', **font)

        for coords, name in zip([(0, 3), (0, 1.8), (4, 9), (assym_coef, excess_coef)], ['N', 'R', 'E', 'Beta']):
            plt.scatter([coords[0]], [coords[1]], label=f'{name}({coords[0]:.2f}, {coords[1]:.2f})')
        plt.legend(loc='best')

        plot_.add_plot(width=NoEscape(r'1\textwidth'), dpi=10000)

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f"""\\alpha = {sample_mean_sym} = {sample_mean}""")
        agn.append(f"""\\\\ \\lambda
            = \\sigma
            = \\sqrt D
            = \\sqrt {{{var}}}
            = {sqrt(var):.2f}
        """)

        agn.append("""\\\\ W_n(x; ~ \\alpha, ~ \\lambda) = \\frac 1 {{\\lambda \\sqrt {{2 \\pi}} }}
            e^{{ - \\frac {{(x - \\alpha)^2}} {{2 \\lambda^2}} }}""")

    doc.generate_pdf('full', clean_tex=False)
latex()
