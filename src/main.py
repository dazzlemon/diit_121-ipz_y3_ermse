"""TODO: DOCSTRING"""
import numpy as np
from approx_fun import approx_fun, fit_args, function_form
from console_solution import print_solution_to_console
from latex_solution import latex_solution
from matplotlib_solution import plot

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
# y = np.array([6, 10, 14, 18, 22, 26, 30, 34, 38, 42])
x = np.arange(1, len(y) + 1)

data = (x, y)

(x_means, y_star, y_means, epsilon) = approx_fun(x, y)
epsilon_min_idx = np.argmin(epsilon)
f_, phi, psi, a_fun, b_fun, f_str = function_form[epsilon_min_idx]

a, b, a_, b_, qs, zs = fit_args(x, y, epsilon_min_idx)

x_ = np.arange(1, len(y), 0.01)
y_ = f_(x_, a, b)

x_arif, x_geom, x_garm = x_means
y1_star, y2_star, y3_star = y_star
y_arif, y_geom, y_garm = y_means

latex_solution(
    data,
    x_means, y_star, y_means,
    epsilon, epsilon_min_idx,
    (a, b), (a_, b_), (qs, zs)
)
print_solution_to_console(
    data,
    phi, psi, a_fun, b_fun, f_str,
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon, epsilon_min_idx,
    a, b, a_, b_,
    qs, zs
)
plot((x, y), (x_, y_), np.array([x_means, y_star]), f_str, (a, b))
