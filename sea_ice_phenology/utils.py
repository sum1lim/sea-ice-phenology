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
