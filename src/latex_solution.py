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

    fpr = '3.3f'# floating precision

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    with doc.create(Section('Lab1')):
        print_means_subsection(doc, 'Step 1', x, 'x', x_means, fpr)

        with doc.create(Subsection('Step 2')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                for i, name in enumerate(['arif', 'geom', 'garm']):
                    agn.append(f"""y_{i + 1}^*
                        = f(x_{{{name}}})
                        = f({x_means[i]:{fpr}})
                        = {y_star[i]:{fpr}} \\\\""")

        print_means_subsection(doc, 'Step 3', y, 'y', y_means, fpr)
        
        with doc.create(Subsection('Step 4')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                mean_names = ["arif", "geom", "garm"]
                y_star_order = [0, 0, 0, 1, 1, 2, 2]
                y_mean_order = [0, 1, 2, 0, 1, 0, 2]
                for i, y_star_i, y_mean_i in zip(range(7), y_star_order, y_mean_order):
                    print_epsilon(
                        agn, i + 1, f"y_{y_star_i + 1}^*", f"y_{{{mean_names[y_mean_i]}}}",
                        y_star[y_star_i], y_means[y_mean_i], epsilon[i], fpr)
        # step 4 = epsilon -> epsilon_min -> f(x, a, b)
        # step 5 -> xyab => qzAB -> y = f(x, a, b) => z = A + Bq
        # step 6 -> qs, zs -> A, B -> a, b
        # step 7 plot xy etc

    doc.generate_pdf('full', clean_tex=False)

def print_epsilon(agn, n, name1, name2, val1, val2, res, fpr):
    agn.append(f"\\varepsilon_{n} = |{name1} - {name2}| = |{val1:{fpr}} - {val2:{fpr}}| = {res:{fpr}} \\\\")

def print_means_subsection(doc, subsection_name, arr, arrname, means, fpr):
    with doc.create(Subsection(subsection_name)):
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            agn.append(f'{arrname}_n = {arrname}_{{{len(arr)}}} = {{{arr[-1]:{fpr}}}} \\\\')
            means_names = [f"{arrname}_{{arif}}", f"{arrname}_{{geom}}", f"{arrname}_{{garm}}"]
            print_means(
                agn, arr[0], arr[-1], means, f"{arrname}_1", f"{arrname}_n", means_names, fpr)

def print_means(agn, val1, val2, results, name1, name2, result_names, fpr):
    for print_fun, res, name in zip([print_mean, print_gmean, print_hmean], results, result_names):
        print_fun(agn, val1, val2, res, name1, name2, name, fpr)

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

def print_gmean(agn, val1, val2, result, name1, name2, result_name, fpr):
    """
    prints geometric mean formula to alignat like
    result_name = f(val1: name1, val2: name2) = result
    with floating precision fpr
    """
    agn.append(f"""{result_name}
        = \\sqrt {{{name1} * {name2}}}
        = \\sqrt {{{val1:{fpr}} * {val2:{fpr}}}}
        = {result:{fpr}} \\\\""")

def print_hmean(agn, val1, val2, result, name1, name2, result_name, fpr):
    """
    prints harmonic mean formula to alignat like
    result_name = f(val1: name1, val2: name2) = result
    with floating precision fpr
    """
    agn.append(f"""{result_name}
        = \\frac {{2 * {name1} * {name2}}} {{{name1} + {name2}}}
        = \\frac {{2 * {val1:{fpr}} * {val2:{fpr}}}} {{{val1:{fpr}} + {val2:{fpr}}}}
        = {result:{fpr}} \\\\""")
