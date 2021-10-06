import matplotlib.pyplot as plt
from console_solution import FP

def plot(x, y, x_, y_, x_means, y_star, f_str, a, b):
    """"
    plots given data
    and three points for means of x and interpolated y's
    """
    plt.scatter(x, y, label='input data')

    plt.scatter(
        x_means, y_star, c='#33ff00',
        label='x_means and theirs approx y values(linear interpolation between neighbours)'
    )
    plt.annotate('x_arif', (x_means[0], y_star[0]))
    plt.annotate('x_geom', (x_means[1], y_star[1]))
    plt.annotate('x_garm', (x_means[2], y_star[2]))

    plt.plot(x_, y_, 'r--', label = f'approximation, f(x, a, b) = {f_str}; a = {a:{FP}}; b = {b:{FP}}')
    plt.legend(loc='upper left')
    plt.show()