"""TODO: DOCSTRING"""
import matplotlib.pyplot as plt
import numpy as np
from pylatex import Document, Section, Subsection, Alignat
from approx_fun import approx_fun, fit_args
from console_solution import print_solution_to_console, FP

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
# y = np.array([6, 10, 14, 18, 22, 26, 30, 34, 38, 42])
x = np.arange(1, len(y) + 1)
(
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon, epsilon_min_idx,
    f
) = approx_fun(x, y)

f_, phi, psi, a_fun, b_fun, f_str = f

a, b, a_, b_, qs, zs = fit_args(x, y, f_, phi, psi, a_fun, b_fun)

x_ = np.arange(1, len(y), 0.01)
y_ = f_(x_, a, b)

def plot():
    plt.scatter(x, y, label='input data')

    x_means = np.array([x_arif, x_geom, x_garm])
    y_star  = np.array([y1_star, y2_star, y3_star])
    plt.scatter(x_means, y_star, c='#33ff00', label='x_means and theirs approx y values(linear interpolation between neighbours)')
    plt.annotate('x_arif', (x_arif, y1_star))
    plt.annotate('x_geom', (x_geom, y2_star))
    plt.annotate('x_garm', (x_garm, y3_star))

    plt.plot(x_, y_, 'r--', label = f'approximation, f(x, a, b) = {f_str}; a = {a:{FP}}; b = {b:{FP}}')
    plt.legend(loc='upper left')
    plt.show() 

n = len(y)
def doc_gen():
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
doc_gen()
print_solution_to_console(
    x, y,
    phi, psi, a_fun, b_fun, f_str,
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon, epsilon_min_idx,
    a, b, a_, b_,
    qs, zs
)