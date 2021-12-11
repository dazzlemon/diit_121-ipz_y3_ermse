"""Lr4"""
import pandas as pd
import numpy as np
from pylatex import Document, NoEscape, Alignat, Package

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

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('booktabs'))# for print_dict_table
    doc.packages.append(Package('float'))# correct position for plot

    print_dict_table(doc, {
        'X': data_x,
        'Y': data_y,
    })

    data_x_smean = np.mean(data_x)
    data_y_smean = np.mean(data_y)

    with doc.create(Alignat(numbering=False, escape=False)) as agn:
        for name, data in zip(['x', 'y'], [data_x_smean, data_y_smean]):
            agn.append(f"""m_{name}
                = \\frac 1 n \\sum\\limits_{{ i=1 }}^n {name}_i
                = {data}
                \\\\
            """)

    doc.generate_pdf('full', clean_tex=True)


latex()
