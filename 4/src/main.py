"""Lr4"""
import pandas as pd
import numpy as np
from pylatex import Document, NoEscape, Alignat, Package
from scipy.stats import f, t
from math import sqrt


def print_dict_table(doc, dict_):
    """dictionary as latex table to pylatex.Document"""
    pd_df = pd.DataFrame(dict_)
    mcf = '|'.join('c' * len(dict_.keys()))
    doc.append(NoEscape(pd_df.to_latex(index=False, escape=False, column_format=mcf)))


def latex():
    """Lr4"""
    data_x = [
        162, 181, 148, 122, 125, 115, 157, 160, 147, 157, 175, 139, 161, 137, 157,
        156, 118, 144, 170, 170, 127, 147, 189, 150, 160, 163, 179, 125, 176, 185,
    ]
    data_y = [
        166, 147, 182, 143, 169, 155, 157, 156, 145, 171, 139, 179, 134, 180, 145,
        141, 188, 137, 132, 180, 182, 182, 161, 143, 139, 124, 118, 152, 176, 112,
    ]
    alpha = 0.01

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('booktabs'))# for print_dict_table
    doc.packages.append(Package('float'))# correct position for plot
    doc.packages.append(Package('amsmath'))

    print_dict_table(doc, {
        'X': data_x,
        'Y': data_y,
    })

    len_x = len(data_x)
    len_y = len(data_y)

    data_x_smean = np.mean(data_x)
    data_y_smean = np.mean(data_y)

    estimator_bias_x = 1 / (len_x - 1) * np.sum((data_x - data_x_smean)**2)
    estimator_bias_y = 1 / (len_y - 1) * np.sum((data_y - data_y_smean)**2)

    alpha_ = alpha / 2 * 100
    fisher_hi = f.ppf(1 - alpha / 2, len_x - 1, len_y - 1)
    fisher_lo = 1 / fisher_hi

    student_hi = 1 / t.ppf(alpha / 2, len_x + len_y - 2)
    student_lo = -student_hi

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        for name, data in zip(['x', 'y'], [data_x_smean, data_y_smean]):
            agn.append(f"""m_{name}
                = \\frac 1 n \\sum\\limits_{{ i=1 }}^n {name}_i
                = {data}
                \\\\
            """)

        for name, data in zip(['x', 'y'], [estimator_bias_x, estimator_bias_y]):
            agn.append(f"""\\widehat S_{name}^2
                = \\frac 1 {{n - 1}} \\sum\\limits_{{ i =1 }}^n {{ ({name}_i - m)^2 }}
                = {data:.2f}
                \\\\
            """)

        agn.append(f"""\\psi_{{est}}
            = \\frac {{\\widehat S_x^2}} {{\\widehat S_y^2}}
            = \\frac {{{estimator_bias_x:.2f}}} {{{estimator_bias_y:.2f}}}
            = {estimator_bias_x / estimator_bias_y:.3f}
            \\\\
        """)

        agn.append(f"""\\psi_{{hi}}
            = F_{{ {alpha_}\\% }}({len_x - 1}, {len_y - 1})
            = {fisher_hi:.3f}
            \\\\
        """)

        agn.append(f"""\\psi_{{lo}}
            = \\frac 1 {{ \\psi_{{hi}} }}
            = \\frac 1 {{{fisher_hi:.3f}}}
            = {fisher_lo:.3f}
            \\\\
        """)

        agn.append(f"""{fisher_lo:.3f}
            < {estimator_bias_x / estimator_bias_y:.3f}
            < {fisher_hi:.3f}
            \\\\
        """)

        if fisher_lo < estimator_bias_x / estimator_bias_y < fisher_hi:
            agn.append(f'H_0~is~correct,~ m_x = m_y ~for~ \\alpha = {alpha}')
        else:
            agn.append(f'H_1~is~correct,~ m_x \\ne m_y ~for~ \\alpha = {alpha}')

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        agn.append(f"""\\\\ \\psi_{{est}}
            = \\frac {{|m_x - m_y|}}
                {{ \\sqrt \\frac {{ (n_1 - 1) * \\widehat S_x^2 + (n_2 - 1) * \\widehat S_y^2 }}
                    {{(n_1 + n_2 - 2)}} }}
                * \\sqrt \\frac {{n_1 n_2}} {{n_1 + n_2}}
            \\\\
            = \\frac {{|{data_x_smean} - {data_y_smean}|}}
                {{ \\sqrt \\frac {{ {len_x - 1} * {estimator_bias_x:.3f} + {len_y - 1} * {estimator_bias_y:.3f} }}
                    {{{len_x + len_y - 2}}} }}
                * \\sqrt \\frac {{ {len_x} * {len_y} }} {{{len_x + len_y}}}
            = {abs(data_x_smean - data_y_smean)
                / sqrt(
                    ( (len_x - 1) * estimator_bias_x + (len_y - 1) * estimator_bias_y ) 
                    / (len_x + len_y - 2)) 
                * sqrt(len_x * len_y / (len_x + len_y)):.3f}
        """)

        agn.append(f"""\\\\ \\psi_{{hi}}
            = t_{{ {alpha_}\\% }}(n_1 + n_2 - 2)
            = t_{{ {alpha_}\\% }}({len_x + len_y - 2})
            = {student_hi:.3f}
        """)

    doc.generate_pdf('full', clean_tex=True)


latex()
