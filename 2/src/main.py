"TODO: DOCSTRING"

import numpy             as np
import matplotlib.pyplot as plt
from scipy          import stats
from more_itertools import pairwise
from tabulate       import tabulate

def np_map(fun, arr):
    """TODO: DOCSTRING"""
    return np.array(list(map(fun , arr)))

def edges_means(edges):
    return np_map(lambda x: (x[0] + x[1]) / 2, pairwise(edges))

def group(data, bin_edges):
    """TODO: DOCSTRING"""
    dlist = sorted(data)
    boundaries_idx = np_map(lambda i: np.argmax(dlist >= i), bin_edges[:-1])[1:]
    return np.array_split(dlist, boundaries_idx)

def sample_mean(grouped_data, bin_edges, freq):
    """Sample mean"""
    bin_means = edges_means(bin_edges)
    return (
        np.sum(bin_means * freq) /
        np.sum(np_map(len, grouped_data))
    )

def pdf_plot(bin_edges, freq):
    """Plots Probability density function"""
    bin_means = edges_means(bin_edges)
    plt.bar(
        bin_means, stats.rv_histogram((freq, bin_edges)).pdf(bin_means),
        label='Probability Density Function',
        width = bin_edges[1] - bin_edges[0]
    )

def freq_poly(bin_edges, freq):
    """Plots Frequency Polygon"""
    bin_means = edges_means(bin_edges)
    plt.plot(bin_means, freq, label='Frequency Polygon')

def cumfreq_plot(bin_edges, data):
    """Plot cummulative frequency"""
    plt.hist(
        data, bins=bin_edges, cumulative=True,
        density=True, label='Cumulative Frequency histogram'
    )

def main():
    """MAIN"""
    # variant 11
    # data = [
    #     180, 155, 149, 176, 181, 146, 105, 191, 163, 116, 113, 182, 149, 195, 147,
    #     146, 113, 185, 155, 149, 180, 131, 184, 198, 119, 122, 160, 153, 109, 158,
    # ]
    data = [
        6.0,  9.1, 8.7, 6.7, 5.4, 10.9, 9.9, 9.4, 9.9, 9.4, 9.2, 9.6,
        8.1,  7.8, 9.5, 8.2, 9.7,  8.1, 8.5, 9.5, 7.9, 8.9, 8.9, 9.7,
        5.7, 11.4, 9.7, 9.2, 9.8, 10.6,
    ]
    amount_bins = 6#5

    width = len(data) / amount_bins
    range_ = (min(data), max(data))

    hist, bin_edges = np.histogram(data, amount_bins)
    grouped = group(data, bin_edges)
    res = stats.cumfreq(sorted(data), numbins=amount_bins, defaultreallimits=range_)

    dict_ = {
        'Range'      : pairwise(bin_edges),
        'Freq'       : hist,
        'CumFreq'    : res.cumcount,
        'FreqDensity': hist / width,
        'Elems'      : grouped,
    }
    print(tabulate(dict_, headers='keys', tablefmt='psql'))
    print(sample_mean(grouped, bin_edges, hist))

    # freq_poly(bin_edges, hist)
    cumfreq_plot(bin_edges, data)
    # pdf_plot(bin_edges, hist / width)

    plt.legend(loc='best')
    plt.show()

if __name__ == "__main__":
    main()
