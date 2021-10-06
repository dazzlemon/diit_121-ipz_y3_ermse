"""TODO: DOCSTRING"""
import numpy as np
from approx_fun import id_, inv
from typing import Tuple

# float precision
FP = '.2f'

def print_fun(prefix, argname, fun):
    """TODO: DOCSTRING"""
    print(prefix, end='')
    if fun == id_:
        print(f'{argname}')
    elif fun == np.log:
        print(f'log({argname})')
    elif fun == np.log10:
        print(f'lg({argname})')
    elif fun == inv:
        print(f'1 / {argname}')

def print_inv(prefix, argname, argval, fun, val):
    """TODO: DOCSTRING"""
    print(prefix, end='')
    if fun == id_:
        print(argname, end='')
    elif fun == np.log:
        print(f'e^{argname:{FP}} = e^{argval:{FP}}', end='')
    elif fun == np.log10:
        print(f'10^{argname:{FP}} = 10^{argval:{FP}}', end='')
    elif fun == inv:
        print(f'1 / {argname:{FP}} = 1 / {argval:{FP}}', end='')
    print(f' = {val:{FP}}')

def print_solution_to_console(
    data: Tuple[np.array, np.array],
    phi, psi, a_fun, b_fun, f_str,
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon, epsilon_min_idx,
    a, b, a_, b_,
    qs, zs
):
    x, y = data
    """TODO: DOCSTRING"""
    n = len(y)
    
    print(f"""x_n
        = x_{n}
        = {x[-1]}""")
    print(f"""x_arif
        = (x_1 + x_n) / 2
        = ({x[0]} + {x[-1]}) / 2
        = {x_arif}""")
    print(f"""x_geom
        = sqrt(x_1 * x_n)
        = sqrt({x[0]} * {x[-1]})
        = {x_geom}""")
    print(f"""x_garm
        = (2 * x_1 * x_n) / (x_1 + x_n)
        = (2 * {x[0]} * {x[-1]}) / ({x[0]} + {x[-1]})
        = {x_garm}""")

    print(f"""y_1^*
        = f(x_arif)
        = f({x_arif})
        = {y1_star}""")
    print(f"""y_2^*
        = f(x_geom)
        = f({x_geom})
        = {y2_star}""")
    print(f"""y_3^*
        = f(x_garm)
        = f({x_garm})
        = {y3_star}""")

    print(f"""y_n
        = y_{n}
        = {y[-1]}""")
    print(f"""y_arif
        = (y_1 + y_n) / 2
        = ({y[0]} + {y[-1]}
        = {y_arif}""")
    print(f"""y_geom
        = sqrt(y1 * y_n)
        = sqrt({y[0]} * {y[-1]})
        = {y_geom}""")
    print(f"""y_garm
        = (2 * y_1 * y_n) / (y1 + yn)
        = (2 * {y[0]} * {y[-1]}) / ({y[0]} + {y[-1]})
        = {y_garm}""")

    for i, eps in enumerate(epsilon, 1):
        print(f"epsilon_{i} = {eps}")

    print(f"epsilon_min = epsilon_{epsilon_min_idx + 1} = {epsilon[epsilon_min_idx]}")
    print(f"f(x, a, b) = f4 = {f_str}")

    print_fun('q = phi(x) = ', 'x', phi)
    print_fun('z = psi(y) = ', 'y', psi)
    print_fun('A = ', 'a', a_fun)
    print_fun('B = ', 'b', b_fun)
    print('z = A + Bq')

    print(f"{qs=}")
    print(f"{zs=}")
    print(f"""B
        = (n * sum(qs * zs) - sum(qs) * sum(zs)) /
            (n * sum(qs ** 2) - sum(qs) ** 2)
        = ({n:{FP}} * {np.sum(qs * zs):{FP}} - {np.sum(qs):{FP}} * {np.sum(zs):{FP}}) /
            ({n:{FP}} * {np.sum(qs ** 2):{FP}} - {np.sum(qs) ** 2:{FP}})
        = {b_:{FP}}""")
    print(f"""A
        = (sum(zs) - B * sum(qs)) / n
        = ({np.sum(zs):{FP}} - {b_:{FP}} * {np.sum(qs):{FP}}) / {n:{FP}}
        = {a_:{FP}}""")

    print_inv('a = ', 'A', a_, a_fun, a)
    print_inv('b = ', 'B', b_, a_fun, b)