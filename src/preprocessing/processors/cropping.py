"""
Raster Cropping Processor

Creates a common simulation window using the spatial
coverage of the DEM, bathymetry and observed inundation data.

The selected simulation window contains both:

1. The earthquake source location
2. The observed inundation region

This allows tsunami propagation to begin at the earthquake
and reach the observed coastal/inundation region.
"""

from __future__ import annotations

import numpy as np


class RasterCropper:

    def __init__(
        self,
        size=(256, 256),
        simulation_mode=True,
        padding=128
    ):

        self.size = size
        self.simulation_mode = simulation_mode
        self.padding = padding

    # ==========================================================
    # GET EARTHQUAKE COORDINATES
    # ==========================================================

    def _get_earthquake_coordinates(
        self,
        earthquake
    ):

        if earthquake is None:
            return None

        if isinstance(
            earthquake,
            dict
        ):

            latitude = earthquake.get(
                "latitude"
            )

            longitude = earthquake.get(
                "longitude"
            )

        else:

            latitude = getattr(
                earthquake,
                "latitude",
                None
            )

            longitude = getattr(
                earthquake,
                "longitude",
                None
            )

        if (
            latitude is None
            or
            longitude is None
        ):

            return None

        try:

            return (
                float(latitude),
                float(longitude)
            )

        except Exception:

            return None

    # ==========================================================
    # GET RASTER BOUNDS
    # ==========================================================

    def _get_bounds(
        self,
        raster
    ):

        if not isinstance(
            raster,
            dict
        ):

            return None

        transform = raster.get(
            "transform"
        )

        data = raster.get(
            "data"
        )

        if (
            transform is None
            or
            data is None
        ):

            return None

        try:

            rows, cols = (
                data.shape[-2:]
            )

            left = transform.c
            top = transform.f

            right = (
                left
                + cols * transform.a
            )

            bottom = (
                top
                + rows * transform.e
            )

            return (
                min(left, right),
                min(bottom, top),
                max(left, right),
                max(bottom, top)
            )

        except Exception:

            return None

    # ==========================================================
    # CONVERT COORDINATES TO PIXEL
    # ==========================================================

    def _coordinate_to_pixel(
        self,
        raster,
        latitude,
        longitude
    ):

        transform = raster.get(
            "transform"
        )

        if transform is None:
            return None

        try:

            col, row = ~transform * (
                longitude,
                latitude
            )

            return (
                float(row),
                float(col)
            )

        except Exception:

            return None

    # ==========================================================
    # FIND VALID REGION
    # ==========================================================

    def _valid_region(
        self,
        raster
    ):

        if not isinstance(
            raster,
            dict
        ):

            return None

        data = raster.get(
            "data"
        )

        if data is None:
            return None

        data = np.asarray(
            data
        )

        if data.ndim != 2:
            return None

        valid = np.isfinite(
            data
        )

        positions = np.argwhere(
            valid
        )

        if positions.size == 0:
            return None

        min_row = int(
            positions[:, 0].min()
        )

        max_row = int(
            positions[:, 0].max()
        )

        min_col = int(
            positions[:, 1].min()
        )

        max_col = int(
            positions[:, 1].max()
        )

        return (
            min_row,
            max_row,
            min_col,
            max_col
        )

    # ==========================================================
    # FIND FLOOD REGION
    # ==========================================================

    def _flood_region(
        self,
        raster
    ):

        if not isinstance(
            raster,
            dict
        ):

            return None

        data = raster.get(
            "data"
        )

        if data is None:
            return None

        data = np.asarray(
            data
        )

        if data.ndim != 2:
            return None

        valid = np.isfinite(
            data
        )

        flooded = (
            valid
            &
            (data > 0.5)
        )

        positions = np.argwhere(
            flooded
        )

        if positions.size == 0:
            return None

        min_row = int(
            positions[:, 0].min()
        )

        max_row = int(
            positions[:, 0].max()
        )

        min_col = int(
            positions[:, 1].min()
        )

        max_col = int(
            positions[:, 1].max()
        )

        return (
            min_row,
            max_row,
            min_col,
            max_col
        )

    # ==========================================================
    # FIND FLOOD MASK CENTRE
    # ==========================================================

    def _flood_mask_center(
        self,
        datasets
    ):

        water_mask = datasets.get(
            "water_mask"
        )

        if not isinstance(
            water_mask,
            dict
        ):

            return None

        data = water_mask.get(
            "data"
        )

        if data is None:
            return None

        data = np.asarray(
            data
        )

        if data.ndim != 2:
            return None

        valid = np.isfinite(
            data
        )

        flooded = (
            valid
            &
            (data > 0.5)
        )

        positions = np.argwhere(
            flooded
        )

        if positions.size == 0:
            return None

        row = float(
            np.mean(
                positions[:, 0]
            )
        )

        col = float(
            np.mean(
                positions[:, 1]
            )
        )

        return (
            row,
            col
        )

    # ==========================================================
    # FIND COMMON VALID REGION
    # ==========================================================

    def _common_valid_region(
        self,
        datasets
    ):

        dem = datasets.get(
            "dem"
        )

        bathymetry = datasets.get(
            "bathymetry"
        )

        if (
            dem is None
            or
            bathymetry is None
        ):

            return None

        dem_region = self._valid_region(
            dem
        )

        bathy_region = self._valid_region(
            bathymetry
        )

        if (
            dem_region is None
            or
            bathy_region is None
        ):

            return None

        min_row = max(
            dem_region[0],
            bathy_region[0]
        )

        max_row = min(
            dem_region[1],
            bathy_region[1]
        )

        min_col = max(
            dem_region[2],
            bathy_region[2]
        )

        max_col = min(
            dem_region[3],
            bathy_region[3]
        )

        if (
            min_row > max_row
            or
            min_col > max_col
        ):

            return None

        return (
            min_row,
            max_row,
            min_col,
            max_col
        )

    # ==========================================================
    # GET EARTHQUAKE PIXEL
    # ==========================================================

    def _get_earthquake_pixel(
        self,
        datasets
    ):

        dem = datasets.get(
            "dem"
        )

        earthquake = datasets.get(
            "earthquake"
        )

        if dem is None:
            return None

        coordinates = (
            self._get_earthquake_coordinates(
                earthquake
            )
        )

        if coordinates is None:
            return None

        latitude, longitude = coordinates

        bounds = self._get_bounds(
            dem
        )

        if bounds is None:
            return None

        min_x, min_y, max_x, max_y = bounds

        if not (
            min_x <= longitude <= max_x
            and
            min_y <= latitude <= max_y
        ):

            print(
                "⚠ Earthquake lies outside DEM bounds."
            )

            return None

        return self._coordinate_to_pixel(
            dem,
            latitude,
            longitude
        )

    # ==========================================================
    # CLAMP WINDOW
    # ==========================================================

    def _clamp_origin(
        self,
        row,
        col,
        rows,
        cols
    ):

        target_rows, target_cols = (
            self.size
        )

        max_row = max(
            0,
            rows - target_rows
        )

        max_col = max(
            0,
            cols - target_cols
        )

        row = max(
            0,
            min(
                int(round(row)),
                max_row
            )
        )

        col = max(
            0,
            min(
                int(round(col)),
                max_col
            )
        )

        return (
            row,
            col
        )

    # ==========================================================
    # DETERMINE SIMULATION WINDOW
    # ==========================================================

    def _get_simulation_window(
        self,
        datasets
    ):

        dem = datasets.get(
            "dem"
        )

        if not isinstance(
            dem,
            dict
        ):

            return (
                0,
                0,
                self.size[0],
                self.size[1]
            )

        dem_data = dem.get(
            "data"
        )

        if dem_data is None:
            return (
                0,
                0,
                self.size[0],
                self.size[1]
            )

        dem_data = np.asarray(
            dem_data
        )

        rows, cols = dem_data.shape

        common_region = (
            self._common_valid_region(
                datasets
            )
        )

        earthquake_pixel = (
            self._get_earthquake_pixel(
                datasets
            )
        )

        flood_region = (
            self._flood_region(
                datasets.get(
                    "water_mask"
                )
            )
        )

        # ------------------------------------------------------
        # Collect important spatial points
        # ------------------------------------------------------

        points = []

        if earthquake_pixel is not None:

            points.append(
                earthquake_pixel
            )

        if flood_region is not None:

            flood_min_row = flood_region[0]
            flood_max_row = flood_region[1]
            flood_min_col = flood_region[2]
            flood_max_col = flood_region[3]

            points.extend(
                [
                    (
                        flood_min_row,
                        flood_min_col
                    ),
                    (
                        flood_min_row,
                        flood_max_col
                    ),
                    (
                        flood_max_row,
                        flood_min_col
                    ),
                    (
                        flood_max_row,
                        flood_max_col
                    )
                ]
            )

        # ------------------------------------------------------
        # If earthquake + flood are available,
        # create a domain containing both.
        # ------------------------------------------------------

        if (
            self.simulation_mode
            and
            len(points) >= 2
        ):

            point_rows = [
                point[0]
                for point in points
            ]

            point_cols = [
                point[1]
                for point in points
            ]

            min_required_row = min(
                point_rows
            )

            max_required_row = max(
                point_rows
            )

            min_required_col = min(
                point_cols
            )

            max_required_col = max(
                point_cols
            )

            required_rows = (
                max_required_row
                - min_required_row
                + 1
            )

            required_cols = (
                max_required_col
                - min_required_col
                + 1
            )

            target_rows = max(
                self.size[0],
                int(
                    required_rows
                    + 2 * self.padding
                )
            )

            target_cols = max(
                self.size[1],
                int(
                    required_cols
                    + 2 * self.padding
                )
            )

            target_rows = min(
                target_rows,
                rows
            )

            target_cols = min(
                target_cols,
                cols
            )

            center_row = (
                min_required_row
                + max_required_row
            ) / 2.0

            center_col = (
                min_required_col
                + max_required_col
            ) / 2.0

            origin_row = (
                center_row
                - target_rows / 2.0
            )

            origin_col = (
                center_col
                - target_cols / 2.0
            )

            if common_region is not None:

                min_row, max_row, min_col, max_col = (
                    common_region
                )

                origin_row = max(
                    min_row,
                    origin_row
                )

                origin_col = max(
                    min_col,
                    origin_col
                )

                # Keep the entire simulation domain
                # inside the common valid region whenever possible.

                if (
                    origin_row + target_rows
                    > max_row + 1
                ):

                    origin_row = (
                        max_row
                        + 1
                        - target_rows
                    )

                if (
                    origin_col + target_cols
                    > max_col + 1
                ):

                    origin_col = (
                        max_col
                        + 1
                        - target_cols
                    )

            origin_row, origin_col = (
                self._clamp_origin(
                    origin_row,
                    origin_col,
                    rows,
                    cols
                )
            )

            return (
                origin_row,
                origin_col,
                target_rows,
                target_cols
            )

        # ------------------------------------------------------
        # Flood-only fallback
        # ------------------------------------------------------

        flood_center = (
            self._flood_mask_center(
                datasets
            )
        )

        if flood_center is not None:

            center_row, center_col = (
                flood_center
            )

            target_rows, target_cols = (
                self.size
            )

            origin_row = (
                center_row
                - target_rows / 2
            )

            origin_col = (
                center_col
                - target_cols / 2
            )

            return (
                *self._clamp_origin(
                    origin_row,
                    origin_col,
                    rows,
                    cols
                ),
                target_rows,
                target_cols
            )

        # ------------------------------------------------------
        # Earthquake-only fallback
        # ------------------------------------------------------

        if earthquake_pixel is not None:

            center_row, center_col = (
                earthquake_pixel
            )

            target_rows, target_cols = (
                self.size
            )

            origin_row = (
                center_row
                - target_rows / 2
            )

            origin_col = (
                center_col
                - target_cols / 2
            )

            return (
                *self._clamp_origin(
                    origin_row,
                    origin_col,
                    rows,
                    cols
                ),
                target_rows,
                target_cols
            )

        # ------------------------------------------------------
        # Common valid region fallback
        # ------------------------------------------------------

        if common_region is not None:

            min_row, max_row, min_col, max_col = (
                common_region
            )

            center_row = (
                min_row + max_row
            ) / 2

            center_col = (
                min_col + max_col
            ) / 2

            target_rows, target_cols = (
                self.size
            )

            origin_row = (
                center_row
                - target_rows / 2
            )

            origin_col = (
                center_col
                - target_cols / 2
            )

            return (
                *self._clamp_origin(
                    origin_row,
                    origin_col,
                    rows,
                    cols
                ),
                target_rows,
                target_cols
            )

        # ------------------------------------------------------
        # DEM centre fallback
        # ------------------------------------------------------

        target_rows, target_cols = (
            self.size
        )

        origin_row = (
            rows / 2
            - target_rows / 2
        )

        origin_col = (
            cols / 2
            - target_cols / 2
        )

        return (
            *self._clamp_origin(
                origin_row,
                origin_col,
                rows,
                cols
            ),
            target_rows,
            target_cols
        )

    # ==========================================================
    # CROP ONE RASTER
    # ==========================================================

    def crop(
        self,
        raster,
        origin_row,
        origin_col,
        target_rows=None,
        target_cols=None
    ):

        if raster is None:
            return None

        if not isinstance(
            raster,
            dict
        ):

            return raster

        if "data" not in raster:
            return raster

        data = raster.get(
            "data"
        )

        if data is None:
            return raster

        data = np.asarray(
            data
        )

        if target_rows is None:
            target_rows = self.size[0]

        if target_cols is None:
            target_cols = self.size[1]

        origin_row = int(
            origin_row
        )

        origin_col = int(
            origin_col
        )

        # ------------------------------------------------------
        # 2D raster
        # ------------------------------------------------------

        if data.ndim == 2:

            rows, cols = (
                data.shape
            )

            end_row = min(
                origin_row + target_rows,
                rows
            )

            end_col = min(
                origin_col + target_cols,
                cols
            )

            cropped = data[
                origin_row:end_row,
                origin_col:end_col
            ]

        # ------------------------------------------------------
        # 3D raster
        # ------------------------------------------------------

        elif data.ndim == 3:

            rows = data.shape[1]
            cols = data.shape[2]

            end_row = min(
                origin_row + target_rows,
                rows
            )

            end_col = min(
                origin_col + target_cols,
                cols
            )

            cropped = data[
                :,
                origin_row:end_row,
                origin_col:end_col
            ]

        else:

            return raster

        raster["data"] = cropped

        raster["shape"] = (
            cropped.shape
        )

        # ------------------------------------------------------
        # Update geospatial transform
        # ------------------------------------------------------

        transform = raster.get(
            "transform"
        )

        if transform is not None:

            try:

                from affine import Affine

                raster["transform"] = (
                    transform
                    * Affine.translation(
                        origin_col,
                        origin_row
                    )
                )

            except Exception:

                pass

        return raster

    # ==========================================================
    # CROP ALL DATASETS
    # ==========================================================

    def crop_all(
        self,
        datasets
    ):

        if datasets is None:
            return datasets

        (
            origin_row,
            origin_col,
            target_rows,
            target_cols
        ) = self._get_simulation_window(
            datasets
        )

        print(
            "Crop window:"
            f" row={origin_row},"
            f" col={origin_col},"
            f" size=({target_rows}, {target_cols})"
        )

        # ------------------------------------------------------
        # Diagnostic information
        # ------------------------------------------------------

        earthquake_pixel = (
            self._get_earthquake_pixel(
                datasets
            )
        )

        flood_center = (
            self._flood_mask_center(
                datasets
            )
        )

        if earthquake_pixel is not None:

            eq_row, eq_col = (
                earthquake_pixel
            )

            print(
                "Earthquake pixel in full DEM:"
                f" row={eq_row:.2f},"
                f" col={eq_col:.2f}"
            )

            print(
                "Earthquake pixel in crop:"
                f" row={eq_row - origin_row:.2f},"
                f" col={eq_col - origin_col:.2f}"
            )

        if flood_center is not None:

            flood_row, flood_col = (
                flood_center
            )

            print(
                "Observed flood centre in crop:"
                f" row={flood_row - origin_row:.2f},"
                f" col={flood_col - origin_col:.2f}"
            )

        cropped = {}

        for name, dataset in (
            datasets.items()
        ):

            if dataset is None:

                print(
                    f"⚠ Skipping {name}: "
                    "dataset unavailable"
                )

                cropped[name] = None

                continue

            if name == "earthquake":

                cropped[name] = dataset

                continue

            cropped[name] = self.crop(
                dataset,
                origin_row,
                origin_col,
                target_rows,
                target_cols
            )

        print(
            "✓ Cropping complete"
        )

        return cropped