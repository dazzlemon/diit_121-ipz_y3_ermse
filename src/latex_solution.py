"""TODO: DOCSTRING"""
from pylatex import Document, Section, Subsection, Alignat
import numpy as np
from typing import Tuple

def latex_solution(
    data: Tuple[np.array, np.array],
    phi, psi, a_fun, b_fun, f_str,
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon, epsilon_min_idx,
    a, b, a_, b_,
    qs, zs
):
    x, y = data
    n = len(y)
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('Lab1')):
        with doc.create(Subsection('Step 1')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(r'x_{arif} = \frac {x_1 + x_n} 2 \\')
                agn.append('x_n = x_{%d} = {%3.3f} \\\\' % (n, x[-1]))
                agn.append("""x_{arif}
                    = \\frac {x_1 + x_n} 2
                    = \\frac {%3.3f + %3.3f} 2
                    = %3.3f \\\\""" % (x[0], x[-1], x_arif))
                agn.append("""x_{geom}
                    = \\sqrt{x_1 * x_n}
                    = \\sqrt{%3.3f * %3.3f}
                    = %3.3f \\\\""" % (x[0], x[-1], x_geom))
                agn.append("""x_{garm}
                    = \\frac {2 * x_1 * x_n} {x_1 + x_n}
                    = \\frac {2 * %3.3f * %3.3f} {%3.3f + %3.3f}
                    = %3.3f""" % (x[0], x[-1], x[0], x[-1], x_garm))

    doc.generate_pdf('full', clean_tex=False)