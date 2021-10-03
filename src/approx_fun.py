from math import sqrt
from operator import itemgetter
import numpy as np

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
    first_after_idx = lambda list_, val: next(x for x, v in enumerate(list_) if v > val)

    x_arif_first_after_idx = first_after_idx(x, x_arif)
    print(x[x_arif_first_after_idx])


    y1_star = float(input("f(%3.3f) = " % x_arif))
    y2_star = float(input("f(%3.3f) = " % x_geom))
    y3_star = float(input("f(%3.3f) = " % x_garm))

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

    f = [
        lambda x, a, b: a + b * x,
        lambda x, a, b: a * b ** x,
        lambda x, a, b: 1 / (a + b * x),
        lambda x, a, b: a + b * np.log10(x),
        lambda x, a, b: a * x ** b,
        lambda x, a, b: a + b / x,
        lambda x, a, b: x / (a + b * x),
    ]

    epsilon_min_idx = min(enumerate(epsilon), key=itemgetter(1))[0]
    f_ = f[epsilon_min_idx]
    return (
        x_arif, x_geom, x_garm,
        y1_star, y2_star, y3_star,
        y_arif, y_geom, y_garm,
        epsilon,
        f_
    )