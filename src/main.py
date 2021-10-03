import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from math import sqrt
from operator import itemgetter

y = np.array([1, 3.07944, 4.29584, 5.15888, 5.82831, 6.37528, 6.83773, 7.23832, 7.59167, 7.90776])
x = np.arange(1, len(y) + 1)

arif = lambda a, b: (a + b) / 2
geom = lambda a, b: sqrt(a * b)
garm = lambda a, b: (2 * a * b) / (a + b)

# 1
x_arif = arif(x[0], x[-1])
x_geom = geom(x[0], x[-1])
x_garm = garm(x[0], x[-1])

# 2
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

fitargs, cov = curve_fit(f_, x, y)
fitdata = f_(x, *fitargs)

plt.scatter(x, y, label = 'a = %3.3f; b = %3.3f' % tuple(fitargs))
plt.plot(x, fitdata, 'r--')

plt.legend(loc='upper left')

plt.show()