"""TODO: DOCSTRING"""
from pylatex import Document, Section, Subsection, Alignat
from approx_fun import function_form

def latex_solution(
    data,
    x_means, y_star, y_means,
    epsilon, epsilon_min_idx,
    args, args_mapped,
    mapped_data
):
    """
    data = [[xs], [ys]]
    xs, ys = [Num]
    """
    x, y = data
    _, phi, psi, a_fun, b_fun, f_str = function_form[epsilon_min_idx]
    n = len(y)
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('Lab1')):
        with doc.create(Subsection('Step 1')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append('x_n = x_{%d} = {%3.3f} \\\\' % (n, x[-1]))
                agn.append("""x_{arif}
                    = \\frac {x_1 + x_n} 2
                    = \\frac {%3.3f + %3.3f} 2
                    = %3.3f \\\\""" % (x[0], x[-1], x_means[0]))
                agn.append("""x_{geom}
                    = \\sqrt{x_1 * x_n}
                    = \\sqrt{%3.3f * %3.3f}
                    = %3.3f \\\\""" % (x[0], x[-1], x_means[1]))
                agn.append("""x_{garm}
                    = \\frac {2 * x_1 * x_n} {x_1 + x_n}
                    = \\frac {2 * %3.3f * %3.3f} {%3.3f + %3.3f}
                    = %3.3f""" % (x[0], x[-1], x[0], x[-1], x_means[2]))

    doc.generate_pdf('full', clean_tex=False)