import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from inspect import getsource
from approx_fun import approx_fun, fit_args, id_, inv

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

def print_fun(prefix, argname, fun):
    print(prefix, end='')
    if fun == id_:
        print(f'{argname}')
    if fun == np.log:
        print(f'log({argname})')
    elif fun == np.log10:
        print(f'lg({argname})')
    elif fun == inv:
        print(f'1 / {argname}')

print_fun('q = phi(x) = ', 'x', phi)
print_fun('z = psi(y) = ', 'y', psi)
print_fun('A = ', 'a', a_fun)
print_fun('B = ', 'b', b_fun)
print('z = A + Bq')

# float precision
fp = '.2f'

print(f"{qs=}")
print(f"{zs=}")
print(f"""B
    = (n * sum(qs * zs) - sum(qs) * sum(zs)) /
        (n * sum(qs ** 2) - sum(qs) ** 2)
    = ({n:{fp}} * {np.sum(qs * zs):{fp}} - {np.sum(qs):{fp}} * {np.sum(zs):{fp}}) /
        ({n:{fp}} * {np.sum(qs ** 2):{fp}} - {np.sum(qs) ** 2:{fp}})
    = {b_:{fp}}""")
print(f"""A
    = (sum(zs) - B * sum(qs)) / n
    = ({np.sum(zs):{fp}} - {b_:{fp}} * {np.sum(qs):{fp}}) / {n:{fp}}
    = {a_:{fp}}""")
print(f"a = {a:{fp}}; b = {b:{fp}}")

plt.scatter(x, y, label='input data')

x_means = np.array([x_arif, x_geom, x_garm])
y_star  = np.array([y1_star, y2_star, y3_star])
plt.scatter(x_means, y_star, c='#33ff00', label='x_means and theirs approx y values(linear interpolation between neighbours)')
plt.annotate('x_arif', (x_arif, y1_star))
plt.annotate('x_geom', (x_geom, y2_star))
plt.annotate('x_garm', (x_garm, y3_star))

plt.plot(x_, y_, 'r--', label = f'approximation, f(x, a, b) = {f_str}; a = {a:{fp}}; b = {b:{fp}}')
plt.legend(loc='upper left')
plt.show()