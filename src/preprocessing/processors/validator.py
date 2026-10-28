"""
Dataset Validator

Checks whether required preprocessing datasets
are available before simulation.

Sentinel-1 and altimetry are optional for now.
"""

from __future__ import annotations


class DatasetValidator:

    # Required for the current pipeline
    REQUIRED_DATASETS = [
        "earthquake",
        "dem",
        "bathymetry",
    ]

    # Optional datasets
    OPTIONAL_DATASETS = [
        "sentinel1",
        "altimetry",
    ]

    # --------------------------------------------------

    def validate(self, datasets):

        if datasets is None:

            raise ValueError(
                "Datasets cannot be None."
            )

        missing = []

        # --------------------------------------------------
        # Required datasets
        # --------------------------------------------------

        for dataset in self.REQUIRED_DATASETS:

            if dataset not in datasets:

                missing.append(dataset)

        if missing:

            raise ValueError(
                f"Missing required datasets: {missing}"
            )

        # --------------------------------------------------
        # Required dataset values
        # --------------------------------------------------

        for dataset in self.REQUIRED_DATASETS:

            if datasets[dataset] is None:

                raise ValueError(
                    f"Required dataset '{dataset}' "
                    f"is None."
                )

        # --------------------------------------------------
        # Optional datasets
        # --------------------------------------------------

        for dataset in self.OPTIONAL_DATASETS:

            if dataset not in datasets:

                print(
                    f"⚠ Optional dataset '{dataset}' "
                    f"not provided."
                )

            elif datasets[dataset] is None:

                print(
                    f"⚠ Optional dataset '{dataset}' "
                    f"skipped."
                )

        return True