"""
interpolation.py
"""

from __future__ import annotations

import numpy as np


class Interpolation:

    @staticmethod
    def nearest(data):

        return np.nan_to_num(data)

    # ---------------------------------------

    @staticmethod
    def fill_missing(data):

        mean = np.nanmean(data)

        return np.where(

            np.isnan(data),

            mean,

            data,

        )

    # ---------------------------------------

    @staticmethod
    def normalize(data):

        minimum = np.min(data)

        maximum = np.max(data)

        return (

            data - minimum

        ) / (

            maximum - minimum + 1e-9

        )