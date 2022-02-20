#!/usr/bin/env python3


def interQuantileMask(series, low=None, middle=None, high=None, multiple=1.5):
    new_series = series.copy()
    Q1 = new_series.quantile(0.25)
    Q3 = new_series.quantile(0.75)
    IQR = Q3 - Q1

    if low != None:
        new_series.mask(new_series < Q1 - multiple * IQR, low, inplace=True)
    if high != None:
        new_series.mask(new_series > Q3 + multiple * IQR, high, inplace=True)
    if middle != None:
        new_series.mask(
            (new_series <= Q3 + multiple * IQR) & (new_series >= Q1 - multiple * IQR),
            middle,
            inplace=True,
        )

    return new_series
