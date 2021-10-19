import numpy as np
from more_itertools import pairwise

def np_map(fun, arr):
    """TODO: DOCSTRING"""
    return np.array(list(map(fun , arr)))

def edges_means(edges):
    return np_map(lambda x: (x[0] + x[1]) / 2, pairwise(edges))