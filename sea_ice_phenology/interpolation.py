#!/usr/bin/env python3
import sys
import math
import pandas as pd
from scipy.ndimage import gaussian_filter1d


def iterative_interpolation(series, method):
    old_series = series.copy()
    for subset_length in range(30):
        new_series = {"system:time_start": [], "interpolated": []}

        for idx, item in enumerate(old_series.iteritems()):
            start = idx - subset_length
            end = idx + subset_length + 1
            if start < 0:
                start = 0
            if end > len(old_series):
                end = len(old_series)

            left_len = len(old_series[start:idx].dropna())
            right_len = len(old_series[idx + 1 : end].dropna())
            timestamp, val = item
            if (
                math.isnan(val)
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
                            old_series[start:end].sample(1)[0]
                        )
                    else:
                        print("Interpolation method not found", file=sys.stderr)
                        exit(1)
                if (idx % 2) == 1:
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
