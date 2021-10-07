"""TODO: DOCSTRING"""
import matplotlib.pyplot as plt
from console_solution import FP
import numpy as np

def plot(data, interpolated_data, interp_points, y_means, f_str, args):
    """"
    plots given data
    and three points for means of x and interpolated y's
    data, interpolated_data, inter_points = [[xs], [ys]]
    xs, ys = [Num]
    """
    plt.scatter(*data, label='input data', s=12)

    plt.scatter(
        interp_points[0], interp_points[1], c='#33ff00',
        label='x_means and theirs approx y values(linear interpolation between neighbours)',
        s=10
    )
    plt.annotate('x_arif', interp_points[:,0], fontsize=10)
    plt.annotate('x_geom', interp_points[:,1], fontsize=10)
    plt.annotate('x_garm', interp_points[:,2], fontsize=10)

    plt.plot(
        *interpolated_data, 'r--',
        label=f'approximation, f(x, a, b) = {f_str}; a = {args[0]:{FP}}; b = {args[1]:{FP}}'
    )
    plt.plot(interpolated_data[0], np.repeat(y_means[0], len(interpolated_data[0])), label=f'y_arif = {y_means[0]}')
    plt.plot(interpolated_data[0], np.repeat(y_means[1], len(interpolated_data[0])), label=f'y_geom = {y_means[1]}')
    plt.plot(interpolated_data[0], np.repeat(y_means[2], len(interpolated_data[0])), label=f'y_garm = {y_means[2]}')
    plt.legend(loc='upper left')
