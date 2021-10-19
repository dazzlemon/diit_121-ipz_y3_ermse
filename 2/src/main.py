"TODO: DOCSTRING"

import numpy             as np
from scipy          import stats
from more_itertools import pairwise
from tabulate       import tabulate
from plots          import plot
from util           import edges_means, np_map
from latex          import latex_solution

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

def print_(data, hist, bin_edges, width, res, grouped):
    """Prints tabular info aboud grouped dataset"""
    dict_ = {
        'Range'      : pairwise(bin_edges),
        'Freq'       : hist,
        'CumFreq'    : res.cumcount,
        'FreqDensity': hist / width,
        'Elems'      : grouped,
    }
    print(tabulate(dict_, headers='keys', tablefmt='psql'))
    print(f'sample mean = {sample_mean(grouped, bin_edges, hist):.2f}')
    print(f'variance = {np.var(data):.2f}')

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

    # width = len(data) / amount_bins
    range_ = (min(data), max(data))
    width = int((range_[1] - range_[0]) / amount_bins)

    hist, bin_edges = np.histogram(data, amount_bins)
    grouped = group(data, bin_edges)
    res = stats.cumfreq(sorted(data), numbins=amount_bins, defaultreallimits=range_)

    # print_(data, hist, bin_edges, width, res, grouped)
    # plot(data, hist, bin_edges, width)
    latex_solution(data, amount_bins, width, bin_edges)

if __name__ == "__main__":
    main()
