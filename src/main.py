"""TODO: DOCSTRING"""
import numpy as np
from approx_fun import approx_fun, fit_args, function_form
from latex_solution import latex_solution

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
x = np.arange(1, len(y) + 1)

data = (x, y)

approx_fun_result = approx_fun(x, y)
epsilon_min_idx = np.argmin(approx_fun_result.errors)
f_, phi, psi, a_fun, b_fun, f_str = function_form[epsilon_min_idx]

a, b, a_, b_, qs, zs = fit_args(x, y, epsilon_min_idx)

x_ = np.arange(1, len(y), 0.01)
y_ = f_(x_, a, b)

latex_solution(
    data, approx_fun_result,
    (a, b), (a_, b_), (qs, zs)
)
