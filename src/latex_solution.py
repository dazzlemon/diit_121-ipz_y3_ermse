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
    data_size = len(y)

    fpr = '3.3f'# floating precision

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    with doc.create(Section('Lab1')):
        with doc.create(Subsection('Step 1')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(f'x_n = x_{{{data_size}}} = {{{x[-1]:{fpr}}}} \\\\')
                print_mean(agn, x[0], x[-1], x_means[0], "x_1", "x_n", "x_{arif}", fpr)
                agn.append(f"""x_{{geom}}
                    = \\sqrt{{x_1 * x_n}}
                    = \\sqrt{{{x[0]:{fpr}} * {x[-1]:{fpr}}}}
                    = {x_means[1]:{fpr}} \\\\""")
                agn.append(f"""x_{{garm}}
                    = \\frac {{2 * x_1 * x_n}} {{x_1 + x_n}}
                    = \\frac 
                        {{2 * {x[0]:{fpr}} * {x[-1]:{fpr}}}}
                        {{{x[0]:{fpr}} + {x[-1]:{fpr}}}}
                    = {x_means[2]:{fpr}}""")

        with doc.create(Subsection('Step 2')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                for i, name in enumerate(['arif', 'geom', 'garm']):
                    agn.append(f"""y_{i + 1}^*
                        = f(x_{{{name}}})
                        = f({x_means[i]:{fpr}})
                        = {y_star[i]:{fpr}} \\\\""")

        with doc.create(Subsection('Step 3')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(f"""y_n
                    = y_{{{data_size}}}
                    = {y[-1]}""")
                agn.append(f"""y_{{arif}}
                    = (y_1 + y_n) / 2
                    = ({y[0]} + {y[-1]}
                    = {y_means[0]}""")
                agn.append(f"""y_geom
                    = sqrt(y1 * y_n)
                    = sqrt({y[0]} * {y[-1]})
                    = {y_means[1]}""")
                agn.append(f"""y_garm
                    = (2 * y_1 * y_n) / (y1 + yn)
                    = (2 * {y[0]} * {y[-1]}) / ({y[0]} + {y[-1]})
                    = {y_means[1]}""")

    doc.generate_pdf('full', clean_tex=False)

def print_mean(agn, val1, val2, result, name1, name2, result_name, fpr):
    """
    prints arithmetic mean formula to alignat like
    result_name = f(val1: name1, val2: name2) = result
    with floating precision fpr
    """
    agn.append(f"""{result_name}
        = \\frac {{{name1} + {name2}}} 2
        = \\frac {{{val1:{fpr}} + {val2:{fpr}}}} 2
        = {result:{fpr}} \\\\""")
