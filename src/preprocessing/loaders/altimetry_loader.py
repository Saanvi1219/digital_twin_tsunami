"""
Altimetry Loader

Loads satellite altimetry measurements from CSV files.
"""

import pandas as pd

from .base_loader import BaseLoader


class AltimetryLoader(BaseLoader):

    def __init__(self, data_dir=None):

        super().__init__(data_dir)

    # --------------------------------------------------

    def download(self):

        raise NotImplementedError(
            "Automatic altimetry download will be implemented later."
        )

    # --------------------------------------------------

    def load(self, filename):

        path = self.get_path(filename)

        return pd.read_csv(path)

    # --------------------------------------------------

    def preprocess(self, filename):

        data = self.load(filename)

        self.validate(data)

        return data

    # --------------------------------------------------

    def validate(self, data):

        if data.empty:

            raise ValueError(
                "Altimetry dataset is empty."
            )

        return True