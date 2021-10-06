from math import sqrt
from operator import itemgetter
import numpy as np
from typing import Callable

# identity function
id_ = lambda x: x
inv = lambda x: 1 / x

# points are sorted by x from lowest to highest
def approx_fun(x, y):
    arif = lambda a, b: (a + b) / 2
    geom = lambda a, b: sqrt(a * b)
    garm = lambda a, b: (2 * a * b) / (a + b)

    # 1
    x_arif = arif(x[0], x[-1])
    x_geom = geom(x[0], x[-1])
    x_garm = garm(x[0], x[-1])

    # 2
    y1_star = np.interp(x_arif, x, y)
    y2_star = np.interp(x_geom, x, y)
    y3_star = np.interp(x_garm, x, y)

    # 3
    y_arif = arif(y[0], y[-1])
    y_geom = geom(y[0], y[-1])
    y_garm = garm(y[0], y[-1])

    # 4
    epsilon = [
        abs(y1_star - y_arif),
        abs(y1_star - y_geom),
        abs(y1_star - y_garm),
        abs(y2_star - y_arif),
        abs(y2_star - y_geom),
        abs(y3_star - y_arif),
        abs(y3_star - y_garm),
    ]

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

    epsilon_min_idx = min(enumerate(epsilon), key=itemgetter(1))[0]
    return (
        x_arif, x_geom, x_garm,
        y1_star, y2_star, y3_star,
        y_arif, y_geom, y_garm,
        epsilon, epsilon_min_idx,
        function_form[epsilon_min_idx]
    )

FloatMap = Callable[[float], float]
def fit_args(xs, ys, f: Callable[[float, float, float], float], phi: FloatMap, psi: FloatMap, a_fun: FloatMap, b_fun: FloatMap):
    #                                           y = f(x, a, b),   q = phi(x),     z = psi(y),            A(a),            B(b)
    qs = phi(xs)
    zs = psi(ys)
    # zs = A(a) + B(b) * qs
    n = len(qs)
    b_ = (n * np.sum(qs * zs) - np.sum(qs) * np.sum(zs)) / \
        (n * np.sum(qs ** 2) - np.sum(qs) ** 2)
    a_ = (np.sum(zs) - b_ * np.sum(qs)) / n
    
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

    a = inverse_fun(a_fun, a_)
    b = inverse_fun(b_fun, b_)

    return a, b, a_, b_, qs, zs
