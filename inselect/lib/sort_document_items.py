from itertools import izip
from operator import itemgetter

import numpy as np

from scipy.signal import argrelmin
from sklearn.neighbors import KernelDensity


def _do_kde(values):
    """Uses kernel denstity estimation to assign values to clusters using
    minima. Returns a generator of ints that are bin numbers.
    """
    # http://stackoverflow.com/a/35151947
    RESCALE = 100
    values = np.array([int(v * RESCALE) for v in values]).reshape(-1, 1)
    kde = KernelDensity().fit(values)

    # Identify minima and use as break points
    samples = np.linspace(0, RESCALE)
    evaluations = kde.score_samples(samples.reshape(-1, 1))
    minima = argrelmin(evaluations)

    # The right-hand edges of bins
    bins = np.append(samples[minima], RESCALE)

    # Cut data
    return (v[0] for v in np.digitize(values, bins, right=True).tolist())


def sort_document_items(items, by_columns):
    """Returns items sorted either by columns or by rows
    """
    if not items:
        # Algorithm is not tolerant of empty values
        return []
    else:
        rects = [i['rect'] for i in items]
        x_bins = _do_kde(r.centre.x for r in rects)
        y_bins = _do_kde(r.centre.y for r in rects)

        if by_columns:
            keys = izip(x_bins, y_bins, (r.left for r in rects))
        else:
            keys = izip(y_bins, x_bins, (r.left for r in rects))
        items_and_keys = sorted(izip(items, keys), key=itemgetter(1))
        return [v[0] for v in items_and_keys]
