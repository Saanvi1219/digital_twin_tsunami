"""
Raster Normalization Processor

IMPORTANT:

Physical raster values are preserved in:

    raster["data"]

Normalized values are stored separately in:

    raster["normalized_data"]

This prevents physical elevation and bathymetry values from
being destroyed before tsunami simulation.
"""

import numpy as np


class RasterNormalizer:

    # ==========================================================
    # NORMALIZE ONE RASTER
    # ==========================================================

    def normalize(self, raster):

        if raster is None:
            return None

        if not isinstance(raster, dict):
            return raster

        if "data" not in raster:
            return raster

        data = raster.get(
            "data"
        )

        if data is None:
            return raster

        data = np.asarray(
            data,
            dtype=np.float32
        )

        finite = np.isfinite(
            data
        )

        if not np.any(finite):

            normalized = np.zeros_like(
                data,
                dtype=np.float32
            )

            raster["normalized_data"] = (
                normalized
            )

            return raster

        minimum = np.nanmin(
            data
        )

        maximum = np.nanmax(
            data
        )

        if maximum == minimum:

            normalized = np.zeros_like(
                data,
                dtype=np.float32
            )

        else:

            normalized = (
                (data - minimum)
                /
                (maximum - minimum)
            )

        normalized = np.nan_to_num(
            normalized,
            nan=0.0,
            posinf=1.0,
            neginf=0.0
        )

        normalized = np.clip(
            normalized,
            0.0,
            1.0
        )

        # ------------------------------------------------------
        # DO NOT overwrite physical data
        # ------------------------------------------------------

        raster["data"] = data

        raster["normalized_data"] = (
            normalized.astype(
                np.float32
            )
        )

        return raster

    # ==========================================================
    # NORMALIZE ALL
    # ==========================================================

    def normalize_all(
        self,
        datasets
    ):

        if datasets is None:

            raise ValueError(
                "Datasets cannot be None."
            )

        processed = {}

        for name, dataset in datasets.items():

            if dataset is None:

                processed[name] = None

                continue

            if name == "earthquake":

                processed[name] = dataset

                continue

            # --------------------------------------------------
            # Binary water mask
            # --------------------------------------------------

            if name == "water_mask":

                if isinstance(
                    dataset,
                    dict
                ):

                    data = dataset.get(
                        "data"
                    )

                    if data is not None:

                        data = np.asarray(
                            data,
                            dtype=np.float32
                        )

                        data = (
                            data > 0.5
                        ).astype(
                            np.float32
                        )

                        dataset["data"] = data

                        dataset[
                            "normalized_data"
                        ] = data.copy()

                processed[name] = dataset

                continue

            processed[name] = (
                self.normalize(
                    dataset
                )
            )

        return processed