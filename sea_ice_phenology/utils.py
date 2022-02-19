#!/usr/bin/env python3


def interQuantileMask(series, low=None, middle=None, high=None):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    if low:
        series.mask(series < Q1 - 1.5 * IQR, low, inplace=True)
    if high:
        series.mask(series > Q3 + 1.5 * IQR, high, inplace=True)
    if middle:
        series.mask(
            (series <= Q3 + 3 * IQR) & (series >= Q1 - 3 * IQR),
            middle,
            inplace=True,
        )

    return series
