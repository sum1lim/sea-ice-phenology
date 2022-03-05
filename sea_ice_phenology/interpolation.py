#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
from math import isnan, sqrt, pi, e
from scipy.ndimage import gaussian_filter1d


def gaussian_weights(size, sigma):
    ret_li = []
    for i in range(size + 1):
        weight = (1 / (sqrt(2 * pi) * (i + 1))) * (
            e ** -((i ** 2) / (2 * (i + 1) ** 2))
        )
        if i == 0:
            ret_li.append(weight)
        else:
            ret_li.insert(0, weight)
            ret_li.append(weight)

    return ret_li


def iterative_interpolation(series, method):
    old_series = series.copy()
    for subset_length in range(30):
        new_series = {"system:time_start": [], "interpolated": []}
        if method == "random":
            weight_li = gaussian_weights(subset_length, 5)

        for idx, item in enumerate(old_series.iteritems()):
            start = idx - subset_length
            end = idx + subset_length + 1

            left_len = len(old_series[start:idx].dropna())
            right_len = len(old_series[idx + 1 : end].dropna())
            timestamp, val = item

            if start < 0 or end > len(old_series):
                new_series["system:time_start"].append(timestamp)
                new_series["interpolated"].append(val)
                continue

            if (
                isnan(val)
                and left_len > 0
                and right_len > 0
                and min(left_len, right_len) / max(left_len, right_len) >= 0.5
            ):
                new_series["system:time_start"].append(timestamp)
                if (idx % 2) == 0:
                    if method == "median":
                        new_series["interpolated"].append(
                            old_series[start:end].median()
                        )
                    elif method == "random":
                        new_series["interpolated"].append(
                            old_series[start:end].sample(1, weights=weight_li)[0]
                        )
                    else:
                        print("Interpolation method not found", file=sys.stderr)
                        exit(1)
                if (idx % 2) == 1:
                    # mean interpolation once every two iterations for variability
                    new_series["interpolated"].append(old_series[start:end].mean())
            else:
                new_series["system:time_start"].append(timestamp)
                new_series["interpolated"].append(val)

        df = pd.DataFrame(new_series)
        df.index = df["system:time_start"]

        new_series = df["interpolated"]
        old_series = new_series

    return new_series


def gaussian_interpolation(series):
    old_series = series.copy()
    new_series = series.copy()
    indices = old_series.dropna().index

    for sigma in range(5):
        new_series = pd.Series(
            gaussian_filter1d(
                new_series.interpolate(
                    "slinear",
                    limit_direction="both",
                    limit_area="inside",
                    limit=sigma + 1,
                ),
                sigma + 1,
            ),
            index=series.index,
        )

        new_series.loc[indices] = old_series[indices]

        indices = old_series.dropna().index
        old_series = new_series

    return new_series


def median_interpolation(series):
    return iterative_interpolation(series, "median")


def random_interpolation(series):
    return iterative_interpolation(series, "random")


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
