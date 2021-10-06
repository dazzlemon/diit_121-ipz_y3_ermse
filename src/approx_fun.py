"""TODO: DOCTSTRING"""
import numpy as np
from scipy.stats import gmean, hmean

# identity function
id_ = lambda x: x
inv = lambda x: 1 / x

function_form = [
    # z = A + Bq
    #                   y = f(x, a, b), q = phi(x),      z = psi(y),     A(a),     B(b), str repr
    (lambda x, a, b:         a + b * x,        id_,             id_,      id_,      id_, 'a + b * x'),
    (lambda x, a, b:        a * b ** x,        id_,          np.log,   np.log,   np.log, 'a * b ^ x'),
    (lambda x, a, b:   1 / (a + b * x),        id_,             inv,      id_,      id_, '1 / (a + b * x)'),
    (lambda x, a, b: a + b * np.log(x),     np.log,             id_,      id_,      id_, 'a + b * log(x)'),
    (lambda x, a, b:        a * x ** b,   np.log10,        np.log10, np.log10,      id_, 'a * x ^ b'),
    (lambda x, a, b:         a + b / x,        inv,             id_,      id_,      id_, 'a + b / x'),
    (lambda x, a, b:   x / (a + b * x),        inv,             inv,      id_,      id_, 'x / (a + b * x)'),
]

def means(arr):
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
    return (x_means, y_star, y_means, epsilon)

# fun(x) = val, returns x, fun = np.log | np.log10 | id_
def inverse_fun(fun, val):
    v_ = 0
    if fun == np.log:
        v_ = np.exp(val)
    elif fun == np.log10:
        v_ = 10 ** val
    else:
    # elif fun == id_:
        v_ = val
    return v_

def fit_args(xs, ys, function_form_n):
    _, phi, psi, a_fun, b_fun, _ = function_form[function_form_n]

    # zs = A(a) + B(b) * qs
    qs = phi(xs)
    zs = psi(ys)

    n = len(qs)
    b_ = (n * np.sum(qs * zs) - np.sum(qs) * np.sum(zs)) / \
        (n * np.sum(qs ** 2) - np.sum(qs) ** 2)
    a_ = (np.sum(zs) - b_ * np.sum(qs)) / n

    a = inverse_fun(a_fun, a_)
    b = inverse_fun(b_fun, b_)

    return a, b, a_, b_, qs, zs
