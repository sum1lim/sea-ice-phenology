import numpy as np

#!/usr/bin/env python3


def interQuantileMask(series, low=None, middle=None, high=None, multiple=1.5):
    low_series = series.copy()
    middle_series = series.copy()
    high_series = series.copy()

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    if low != None:
        low_series.mask(low_series < Q1 - multiple * IQR, low, inplace=True)
    if high != None:
        high_series.mask(high_series > Q3 + multiple * IQR, high, inplace=True)
    if middle != None:
        middle_series.mask(
            (middle_series <= Q3 + multiple * IQR)
            & (middle_series >= Q1 - multiple * IQR),
            middle,
            inplace=True,
        )

    low_series = low_series.drop(low_series[low_series != low].index)
    middle_series = middle_series.drop(middle_series[middle_series != middle].index)
    high_series = high_series.drop(high_series[high_series != high].index)

    series.loc[low_series.index] = low_series[low_series.index]
    series.loc[middle_series.index] = middle_series[middle_series.index]
    series.loc[high_series.index] = high_series[high_series.index]

    return series


def hampel_filter(input_series, window_size, n_sigmas=3):
    """
    By Eryk Lewinson: https://towardsdatascience.com/outlier-detection-with-hampel-filter-85ddf523c73d
    """

    n = len(input_series)
    new_series = input_series.copy()
    k = 1.4826  # scale factor for Gaussian distribution

    indices = []

    # possibly use np.nanmedian
    for i in range((window_size), (n - window_size)):
        x0 = np.median(input_series[(i - window_size) : (i + window_size)])
        S0 = k * np.median(
            np.abs(input_series[(i - window_size) : (i + window_size)] - x0)
        )
        if np.abs(input_series[i] - x0) > n_sigmas * S0:
            new_series[i] = x0
            indices.append(i)

    return new_series, indices
