"""TODO: DOCSTRING"""
import numpy as np
from approx_fun import approx_fun, fit_args
from latex_solution import latex_solution

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
x = np.arange(1, len(y) + 1)

approx_fun_result = approx_fun(x, y)
epsilon_min_idx = np.argmin(approx_fun_result.errors)
fit_args_result = fit_args(x, y, epsilon_min_idx)
latex_solution((x, y), approx_fun_result, fit_args_result)
