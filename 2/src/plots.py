import matplotlib.pyplot as plt
from scipy import stats
from util import edges_means

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

def plot(data, hist, bin_edges, width):
    """Plots representations for grouped data"""
    plt.subplot(2, 2, 1)
    freq_poly(bin_edges, hist)
    plt.legend(loc='best')

    plt.subplot(2, 2, 2)
    cumfreq_plot(bin_edges, data)
    plt.legend(loc='best')

    plt.subplot(2, 2, 3)
    pdf_plot(bin_edges, hist / width)
    plt.legend(loc='best')

    plt.show()