import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from inspect import getsource
from approx_fun import approx_fun

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
x = np.arange(1, len(y) + 1)
(
    x_arif, x_geom, x_garm,
    y1_star, y2_star, y3_star,
    y_arif, y_geom, y_garm,
    epsilon,
    f_
) = approx_fun(x, y)

print(f"{x_arif=}")
print(f"{x_geom=}")
print(f"{x_garm=}")

print(f"{y1_star=}")
print(f"{y2_star=}")
print(f"{y3_star=}")

print(f"{y_arif=}")
print(f"{y_geom=}")
print(f"{y_garm=}")

print(f"{epsilon=}")

print(f"{getsource(f_)}")

fitargs, cov = curve_fit(f_, x, y)
fitdata = f_(x, *fitargs)
print("a = %3.3f; b = %3.3f" % tuple(fitargs))

plt.scatter(x, y)
plt.plot(x, fitdata, 'r--', label = 'a = %3.3f; b = %3.3f' % tuple(fitargs))

plt.legend(loc='upper left')

plt.show()