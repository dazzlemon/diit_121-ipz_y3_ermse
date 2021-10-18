"TODO: DOCSTRING"

import numpy as np
from scipy import stats
from more_itertools import pairwise

def np_map(fun, arr):
    """TODO: DOCSTRING"""
    return np.array(list(map(fun , arr)))

def group(datalist, amount_of_intervals):
    """TODO: DOCSTRING"""
    dlist = sorted(datalist)

    dmin = dlist[0]
    dmax = dlist[-1]

    interval_width = (dmax - dmin) / amount_of_intervals# h

    interval_boundaries = np.arange(amount_of_intervals + 1) * interval_width + dmin

    boundaries_idx = np_map(lambda i: np.argmax(dlist >= i), interval_boundaries[:-1])[1:]

    return np.array_split(dlist, boundaries_idx), interval_boundaries



# def eval_distribution():



def main():
    """MAIN"""
    # variant 11
    data = [
        180, 155, 149, 176, 181, 146, 105, 191, 163, 116, 113, 182, 149, 195, 147,
        146, 113, 185, 155, 149, 180, 131, 184, 198, 119, 122, 160, 153, 109, 158,
    ]

    grouped, boundaries = group(data, 5)
    res = stats.cumfreq(sorted(data), numbins=5, defaultreallimits=(min(data), max(data)))

    print("range         size", "cumfreq", "elems")
    for i, c, bounds in zip(grouped, res.cumcount, pairwise(boundaries)):
        print(f"[{bounds[0]};{bounds[1]}]", f"{len(i)}  ", f"{c:.0f}          ", i)

if __name__ == "__main__":
    main()