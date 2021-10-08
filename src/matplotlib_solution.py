"""TODO: DOCSTRING"""
import matplotlib.pyplot as plt
import numpy as np
from approx_fun import ApproxFunResult, FitArgsResult, function_form

FP = '3.3f'

def plot(data, approx_fun_result: ApproxFunResult, fit_args_result: FitArgsResult):
    """"
    plots given data
    and three points for means of x and interpolated y's
    data, interpolated_data, inter_points = [[xs], [ys]]
    xs, ys = [Num]
    """

    error_argmin = np.argmin(approx_fun_result.errors)
    func_lambda = function_form[error_argmin][0]
    x_points = np.arange(1, data[0][-1], 0.01)
    interpolated_data = (x_points, func_lambda(x_points, *fit_args_result.args))

    interp_points = np.array([approx_fun_result.x_means, approx_fun_result.y_star])
    f_str = function_form[error_argmin][5]
    args = fit_args_result.args

    input_data_markersize = 12
    x_means_markersize = 10
    x_means_fontsize = 10

    plt.scatter(*data, label='input data', s=input_data_markersize)
    plt.scatter(
        interp_points[0], interp_points[1], c='#33ff00',
        label='x_means and theirs approx y values(linear interpolation between neighbours)',
        s=x_means_markersize
    )
    for i, str_ in enumerate(['x_arif', 'x_geom', 'x_garm']):
        plt.annotate(str_, interp_points[:,i], fontsize=x_means_fontsize)

    plt.plot(
        *interpolated_data, 'r--',
        label=f'approximation, f(x, a, b) = {f_str}; a = {args[0]:{FP}}; b = {args[1]:{FP}}'
    )
    for i, str_ in enumerate(['y_arif', 'y_geom', 'y_garm']):
        plt.plot(
            interpolated_data[0], np.repeat(approx_fun_result.y_means[i],
            len(interpolated_data[0])), label=f'{str_} = {approx_fun_result.y_means[i]}')
    plt.legend(loc='upper left')
