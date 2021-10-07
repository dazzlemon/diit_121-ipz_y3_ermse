"""TODO: DOCSTRING"""
from pylatex import Document, Section, Subsection, Alignat, Figure, NoEscape
from approx_fun import (function_form, id_, inv,
    fun_exp, fun_frac, fun_frac2, fun_hyperbole, fun_linear, fun_log, fun_pow)
import numpy as np
from matplotlib_solution import plot
import matplotlib

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
    f_, phi, psi, a_fun, b_fun, f_str = function_form[epsilon_min_idx]

    fpr = '3.3f'# floating precision

    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    with doc.create(Section('Finding function form')):
        print_means_subsection(doc, 'Mean values of x', x, 'x', x_means, fpr)

        with doc.create(Subsection('Interpolated y values for mean values of x')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                for i, name in enumerate(['arif', 'geom', 'garm']):
                    agn.append(f"""y_{i + 1}^*
                        = f(x_{{{name}}})
                        = f({x_means[i]:{fpr}})
                        = {y_star[i]:{fpr}} \\\\""")

        print_means_subsection(doc, 'Mean values of y', y, 'y', y_means, fpr)

        with doc.create(Subsection('Choosing function form according to epsilon error')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                mean_names = ["arif", "geom", "garm"]
                y_star_order = [0, 0, 0, 1, 1, 2, 2]
                y_mean_order = [0, 1, 2, 0, 1, 0, 2]
                for i, y_star_i, y_mean_i in zip(range(7), y_star_order, y_mean_order):
                    print_epsilon(
                        agn, i + 1, f"y_{y_star_i + 1}^*", f"y_{{{mean_names[y_mean_i]}}}",
                        y_star[y_star_i], y_means[y_mean_i], epsilon[i], fpr)
                agn.append(f"""\\Rightarrow \\\\
                    \\varepsilon_{{min}}
                    = \\varepsilon_{epsilon_min_idx + 1}
                    = {epsilon[epsilon_min_idx]:{fpr}} \\\\""")
                agn.append(f"""\\Rightarrow \\\\
                    y \\approx {f_str}""")

    with doc.create(Section('Fitting arguments')):
        with doc.create(Subsection('Transformation of coordinates from xOy to qOz')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(fun_str('q = phi(x) = ', 'x', phi))
                agn.append(fun_str('z = psi(y) = ', 'y', psi))
                agn.append(fun_str('A = ', 'a', a_fun))
                agn.append(fun_str('B = ', 'b', b_fun))
                agn.append('z = A + Bq')

        with doc.create(Subsection('Fitting arguments for linear function in qOz')):
            qs, zs = mapped_data
            a_, b_ = args_mapped
            a, b   = args
            n = len(x)
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(f"""B
                    = \\frac {{n * \\sum\\limits_{{i = 1}}^n {{q_i * z_i}} - \\sum\\limits_{{i = 1}}^n {{q_i}} * \\sum\\limits_{{i = 1}}^n {{z_i}}}}
                        {{n * \\sum\\limits_{{i = 1}}^n {{q_i^2}} - (\\sum\\limits_{{i = 1}}^n {{q_i}}) ^ 2}}
                    = \\frac {{{n} * {np.sum(qs * zs):{fpr}} - {np.sum(qs):{fpr}} * {np.sum(zs):{fpr}}}}
                        {{{n} * {np.sum(qs ** 2):{fpr}} - {np.sum(qs) ** 2:{fpr}}}}
                    = {b_:{fpr}} \\\\""")
                agn.append(f"""A
                    = \\frac {{\\sum\\limits_{{i = 1}}^n {{z_i}} - B * \\sum\\limits_{{i = 1}}^{{n}} {{q_i}}}} n
                    = \\frac {{{np.sum(zs):{fpr}} - {b_:{fpr}} * {np.sum(qs):{fpr}}}} {{{n}}}
                    = {a_:{fpr}} \\\\""")

        with doc.create(Subsection('Mapping arguments back to xOy')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(inv_fun_str('a = ', 'A', a_, a_fun, a, fpr))
                agn.append(inv_fun_str('b = ', 'B', b_, a_fun, b, fpr))
                agn.append(fun2_str('y \\approx', f'{a:{fpr}}', f'{b:{fpr}}', f_))

            with doc.create(Figure(position='htbp')) as plot_:
                x_ = np.arange(1, len(y), 0.01)
                y_ = f_(x_, a, b)
                font = {'size'   : 6}
                matplotlib.rc('font', **font)
                plot(data, (x_, y_), np.array([x_means, y_star]), f_str, args)
                plot_.add_plot(width=NoEscape(r'1\textwidth'), dpi=10000)

    doc.generate_pdf('full', clean_tex=False)

def fun2_str(prefix, arg1, arg2, fun):
    result = prefix
    if fun == fun_linear:
        result += f'{arg1} + {arg2} * x'
    if fun == fun_exp:
        result += f'{arg1} * {arg2} ^ x'
    if fun == fun_frac:
        result += f'1 / ({arg1} + {arg2} * x)'
    if fun == fun_log:
        result += f'{arg1} + {arg2} * log(x)'
    if fun == fun_pow:
        result += f'{arg1} * x ^ {arg2}'
    if fun == fun_hyperbole:
        result += f'{arg1} + {arg2} / x'
    if fun == fun_frac2:
        result += f'x / ({arg1} + {arg2} * x)'
    return result

def inv_fun_str(prefix, argname, argval, fun, val, fpr):
    """TODO: DOCSTRING"""
    result = prefix
    if fun == id_:
        result += argname
    elif fun == np.log:
        result += f'e^{argname:{fpr}} = e^{argval:{fpr}}'
    elif fun == np.log10:
        result += f'10^{argname:{fpr}} = 10^{argval:{fpr}}'
    elif fun == inv:
        result += f'1 / {argname:{fpr}} = 1 / {argval:{fpr}}'
    result += f' = {val:{fpr}} \\\\'
    return result

def fun_str(prefix, argname, fun):
    """TODO: DOCSTRING"""
    result = prefix
    if fun == id_:
        result += f'{argname} \\\\'
    elif fun == np.log:
        result += f'log({argname}) \\\\'
    elif fun == np.log10:
        result += f'lg({argname}) \\\\'
    elif fun == inv:
        result += f'\\frac 1 {{{argname}}} \\\\'
    return result

def print_epsilon(agn, n, name1, name2, val1, val2, res, fpr):
    agn.append(f"""\\varepsilon_{n}
        = |{name1} - {name2}| = |{val1:{fpr}} - {val2:{fpr}}| = {res:{fpr}} \\\\""")

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
