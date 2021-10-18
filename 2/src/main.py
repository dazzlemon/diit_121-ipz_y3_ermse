"TODO: DOCSTRING"

import numpy             as np
import matplotlib.pyplot as plt
from scipy          import stats
from more_itertools import pairwise
from tabulate       import tabulate

def np_map(fun, arr):
    """TODO: DOCSTRING"""
    return np.array(list(map(fun , arr)))

def group(data, bin_edges):
    """TODO: DOCSTRING"""
    dlist = sorted(data)
    boundaries_idx = np_map(lambda i: np.argmax(dlist >= i), bin_edges[:-1])[1:]
    return np.array_split(dlist, boundaries_idx)

def pdf():
    """Probability density function"""
    freq_density = freq / width

def freq_poly(bin_edges, freq):
    bin_means = np_map(lambda x: (x[0] + x[1]) / 2, pairwise(bin_edges))
    plt.plot(bin_means, freq)

def main():
    """MAIN"""
    # variant 11
    data = [
        180, 155, 149, 176, 181, 146, 105, 191, 163, 116, 113, 182, 149, 195, 147,
        146, 113, 185, 155, 149, 180, 131, 184, 198, 119, 122, 160, 153, 109, 158,
    ]

    amount_bins = 5
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
    
    freq_poly(bin_edges, hist)
    plt.show()

if __name__ == "__main__":
    main()
