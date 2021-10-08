"""TODO: DOCTSTRING"""
from dataclasses import dataclass
import numpy as np
from scipy.stats import gmean, hmean

# identity function
id_ = lambda x: x
inv = lambda x: 1 / x

fun_linear    = lambda x, a, b:         a + b * x
fun_exp       = lambda x, a, b:        a * b ** x
fun_frac      = lambda x, a, b:   1 / (a + b * x)
fun_log       = lambda x, a, b: a + b * np.log(x)
fun_pow       = lambda x, a, b:        a * x ** b
fun_hyperbole = lambda x, a, b:         a + b / x
fun_frac2     = lambda x, a, b:   x / (a + b * x)

function_form = [
    # z = A + Bq
    # y = f(x, a, b), q = phi(x),      z = psi(y),     A(a),     B(b), str repr
    (fun_linear     ,        id_,             id_,      id_,      id_, 'a + b * x'),
    (fun_exp        ,        id_,          np.log,   np.log,   np.log, 'a * b ^ x'),
    (fun_frac       ,        id_,             inv,      id_,      id_, '1 / (a + b * x)'),
    (fun_log        ,     np.log,             id_,      id_,      id_, 'a + b * log(x)'),
    (fun_pow        ,   np.log10,        np.log10, np.log10,      id_, 'a * x ^ b'),
    (fun_hyperbole  ,        inv,             id_,      id_,      id_, 'a + b / x'),
    (fun_frac2      ,        inv,             inv,      id_,      id_, 'x / (a + b * x)'),
]

@dataclass
class ApproxFunResult:
    """Represents return from approx_fun"""
    x_means: np.array
    y_star:  np.array
    y_means: np.array
    errors:  np.array

def means(arr):
    """Returns array of arithmetic, geometric and harmonic means for argument array"""
    return np.array([
        np.mean(arr),
        gmean(arr),
        hmean(arr),
    ])

def approx_fun(xs_arr, ys_arr):
    """
    Returns form of function that fits given data the best,
    also returns solution steps
    """
    x_means = means([xs_arr[0], xs_arr[-1]])
    y_means = means([ys_arr[0], ys_arr[-1]])
    y_star  = np.interp(x_means, xs_arr, ys_arr)
    epsilon = np.abs(
        np.take(y_star,  [0, 0, 0, 1, 1, 2, 2]) -
        np.take(y_means, [0, 1, 2, 0, 1, 0, 2])
    )
    return ApproxFunResult(x_means, y_star, y_means, epsilon)

def inverse_fun(fun, val):
    """fun(x) = val, returns x, fun = np.log | np.log10 | id_"""
    inv_val = 0
    if fun == np.log:
        inv_val = np.exp(val)
    elif fun == np.log10:
        inv_val = 10 ** val
    else:
    # elif fun == id_:
        inv_val = val
    return inv_val

def fit_args(xs_arr, ys_arr, function_form_n):
    """
    Finds args for function_form #n that fit given data the best,
    also returns solution steps
    """
    _, phi, psi, a_fun, b_fun, _ = function_form[function_form_n]

    # zs = A(a) + B(b) * qs
    phi_xs = phi(xs_arr)
    psi_ys = psi(ys_arr)

    data_len = len(phi_xs)
    mapped_arg1 = (
        (data_len * np.sum(phi_xs * psi_ys) - np.sum(phi_xs) * np.sum(psi_ys)) /
        (data_len * np.sum(phi_xs ** 2)     - np.sum(phi_xs) ** 2)
    )
    mapped_arg2 = (np.sum(psi_ys) - mapped_arg1 * np.sum(phi_xs)) / data_len

    arg1 = inverse_fun(a_fun, mapped_arg2)
    arg2 = inverse_fun(b_fun, mapped_arg1)

    return arg1, arg2, mapped_arg2, mapped_arg1, phi_xs, psi_ys
