"""TODO: DOCSTRING"""
import matplotlib.pyplot as plt
from console_solution import FP

def plot(data, interpolated_data, interp_points, f_str, args):
    """"
    plots given data
    and three points for means of x and interpolated y's
    data, interpolated_data, inter_points = [[xs], [ys]]
    xs, ys = [Num]
    """
    plt.scatter(*data, label='input data')

    plt.scatter(
        interp_points[0], interp_points[1], c='#33ff00',
        label='x_means and theirs approx y values(linear interpolation between neighbours)'
    )
    plt.annotate('x_arif', interp_points[:,0])
    plt.annotate('x_geom', interp_points[:,1])
    plt.annotate('x_garm', interp_points[:,2])

    plt.plot(
        *interpolated_data, 'r--',
        label = f'approximation, f(x, a, b) = {f_str}; a = {args[0]:{FP}}; b = {args[1]:{FP}}'
    )
    plt.legend(loc='upper left')
    plt.show()
