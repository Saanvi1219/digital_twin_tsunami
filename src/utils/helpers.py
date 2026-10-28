"""
==================================================
Helper Functions
==================================================
"""

import numpy as np


def normalize(array):

    array = np.asarray(array)

    minimum = np.nanmin(array)

    maximum = np.nanmax(array)

    if maximum - minimum == 0:

        return np.zeros_like(array)

    return (array - minimum) / (maximum - minimum)


def inverse_normalize(array):

    return 1 - normalize(array)


def euclidean_distance(x1, y1, x2, y2):

    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def exponential_distance_decay(distance, d0=100):

    return np.exp(-distance / d0)


def classify_value(value, categories):

    for limits, label in categories.items():

        if limits[0] <= value <= limits[1]:

            return label

    return "Unknown"


def safe_divide(a, b):

    if b == 0:

        return 0

    return a / b