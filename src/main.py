import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from inspect import getsource
from approx_fun import approx_fun, fit_args

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
# y = np.array([6, 10, 14, 18, 22, 26, 30, 34, 38, 42])
x = np.arange(1, len(y) + 1)
(
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon,
    f
) = approx_fun(x, y)

f_, phi, psi, a_fun, b_fun, f_str = f

a, b = fit_args(x, y, f_, phi, psi, a_fun, b_fun)
# fitargs, cov = curve_fit(f_, x, y)
# a, b = tuple(fitargs)

x_ = np.arange(1, len(y), 0.01)
# y_ = f_(x_, *fitargs)
y_ = f_(x_, a, b)

print(f"""x_n
    = x_{len(y)}
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

print(f"""{y_arif=}""")
print(f"""{y_geom=}""")
print(f"""{y_garm=}""")

print(f"{epsilon=}")

print(f"f(x, a, b) = {f_str}")

# print("a = %3.3f; b = %3.3f" % tuple(fitargs))
print("a = %3.3f; b = %3.3f" % (a, b))

plt.scatter(x, y, label='input data')

x_means = np.array([x_arif, x_geom, x_garm])
y_star  = np.array([y1_star, y2_star, y3_star])
plt.scatter(x_means, y_star, c='#33ff00', label='x_means and theirs approx y values(linear interpolation between neighbours)')

plt.plot(x_, y_, 'r--', label = f'approximation, f(x, a, b) = {f_str};' +' a = %3.3f; b = %3.3f' % (a, b))
# plt.plot(x_, y_, 'r--', label = 'a = %3.3f; b = %3.3f' % tuple(fitargs))
plt.legend(loc='upper left')
plt.show()