"""
Raster Alignment Processor

Aligns raster datasets to the DEM reference grid.

Uses rasterio CRS-aware reprojection whenever spatial metadata
is available.

Categorical/binary masks use nearest-neighbour resampling.
Continuous rasters use bilinear resampling.
"""

import numpy as np

try:

    from rasterio.warp import (
        reproject,
        Resampling,
        transform_bounds
    )

    RASTERIO_AVAILABLE = True

except ImportError:

    RASTERIO_AVAILABLE = False


class RasterAlignment:

    def __init__(self):

        self.reference = None

    # ==========================================================
    # REFERENCE
    # ==========================================================

    def set_reference(self, raster):

        self.reference = raster

    # ==========================================================
    # GET BOUNDS
    # ==========================================================

    def _get_bounds(
        self,
        raster,
        target_crs=None
    ):

        if not isinstance(raster, dict):

            return None

        bounds = raster.get(
            "bounds"
        )

        crs = raster.get(
            "crs"
        )

        if bounds is None:

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

                bounds = (
                    min(left, right),
                    min(bottom, top),
                    max(left, right),
                    max(bottom, top)
                )

            except Exception:

                return None

        # ------------------------------------------------------
        # Transform bounds to target CRS
        # ------------------------------------------------------

        if (
            target_crs is not None
            and
            crs is not None
            and
            str(crs) != str(target_crs)
        ):

            try:

                return transform_bounds(
                    crs,
                    target_crs,
                    bounds.left,
                    bounds.bottom,
                    bounds.right,
                    bounds.top,
                    densify_pts=21
                )

            except Exception:

                return None

        try:

            return (
                bounds.left,
                bounds.bottom,
                bounds.right,
                bounds.top
            )

        except AttributeError:

            return bounds

    # ==========================================================
    # SPATIAL OVERLAP
    # ==========================================================

    def _has_spatial_overlap(
        self,
        raster,
        reference
    ):

        reference_crs = reference.get(
            "crs"
        )

        source_bounds = self._get_bounds(
            raster,
            target_crs=reference_crs
        )

        reference_bounds = self._get_bounds(
            reference
        )

        if (
            source_bounds is None
            or
            reference_bounds is None
        ):

            return True

        source_left = source_bounds[0]
        source_bottom = source_bounds[1]
        source_right = source_bounds[2]
        source_top = source_bounds[3]

        reference_left = reference_bounds[0]
        reference_bottom = reference_bounds[1]
        reference_right = reference_bounds[2]
        reference_top = reference_bounds[3]

        horizontal_overlap = (
            source_left < reference_right
            and
            source_right > reference_left
        )

        vertical_overlap = (
            source_bottom < reference_top
            and
            source_top > reference_bottom
        )

        return (
            horizontal_overlap
            and
            vertical_overlap
        )

    # ==========================================================
    # ALIGN ONE RASTER
    # ==========================================================

    def align(
        self,
        raster,
        is_mask=False,
        name="raster"
    ):

        if self.reference is None:

            raise RuntimeError(
                "Reference raster not set."
            )

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

        reference_data = (
            self.reference.get(
                "data"
            )
        )

        if reference_data is None:

            return raster

        data = np.asarray(
            data
        )

        ref_shape = (
            np.asarray(
                reference_data
            ).shape
        )

        # ------------------------------------------------------
        # Already aligned
        # ------------------------------------------------------

        if data.shape == ref_shape:

            raster["shape"] = data.shape

            return raster

        source_crs = raster.get(
            "crs"
        )

        source_transform = raster.get(
            "transform"
        )

        reference_crs = self.reference.get(
            "crs"
        )

        reference_transform = (
            self.reference.get(
                "transform"
            )
        )

        # ------------------------------------------------------
        # CRS-aware reprojection
        # ------------------------------------------------------

        if (
            RASTERIO_AVAILABLE
            and
            source_crs is not None
            and
            source_transform is not None
            and
            reference_crs is not None
            and
            reference_transform is not None
            and
            data.ndim == 2
            and
            len(ref_shape) == 2
        ):

            print(
                f"\n[ALIGNMENT] {name}"
            )

            print(
                f"Source CRS      : {source_crs}"
            )

            print(
                f"Reference CRS   : {reference_crs}"
            )

            print(
                f"Source shape    : {data.shape}"
            )

            print(
                f"Reference shape : {ref_shape}"
            )

            source_bounds = self._get_bounds(
                raster,
                target_crs=reference_crs
            )

            reference_bounds = self._get_bounds(
                self.reference
            )

            print(
                f"Source bounds in DEM CRS : "
                f"{source_bounds}"
            )

            print(
                f"DEM bounds                : "
                f"{reference_bounds}"
            )

            # --------------------------------------------------
            # Check geographic overlap
            # --------------------------------------------------

            if not self._has_spatial_overlap(
                raster,
                self.reference
            ):

                print(
                    f"⚠ {name} has NO geographic "
                    "overlap with DEM."
                )

                raster["data"] = None
                raster["shape"] = None

                return raster

            print(
                f"✓ {name} overlaps DEM."
            )

            # --------------------------------------------------
            # Initialize with NaN
            # --------------------------------------------------

            aligned = np.full(
                ref_shape,
                np.nan,
                dtype=np.float32
            )

            if is_mask:

                resampling = (
                    Resampling.nearest
                )

            else:

                resampling = (
                    Resampling.bilinear
                )

            # --------------------------------------------------
            # Reproject
            # --------------------------------------------------

            reproject(
                source=data.astype(
                    np.float32
                ),

                destination=aligned,

                src_transform=(
                    source_transform
                ),

                src_crs=source_crs,

                dst_transform=(
                    reference_transform
                ),

                dst_crs=reference_crs,

                resampling=resampling,

                src_nodata=raster.get(
                    "nodata"
                ),

                dst_nodata=np.nan
            )

            # --------------------------------------------------
            # Valid pixel check
            # --------------------------------------------------

            valid_pixels = np.isfinite(
                aligned
            )

            valid_count = int(
                valid_pixels.sum()
            )

            total_pixels = (
                aligned.size
            )

            print(
                f"Valid pixels   : "
                f"{valid_count}/{total_pixels}"
            )

            if valid_count == 0:

                print(
                    f"⚠ {name} reprojection "
                    "produced ZERO valid pixels."
                )

                raster["data"] = None
                raster["shape"] = None

                return raster

            # --------------------------------------------------
            # Statistics
            # --------------------------------------------------

            print(
                f"Min            : "
                f"{np.nanmin(aligned)}"
            )

            print(
                f"Max            : "
                f"{np.nanmax(aligned)}"
            )

            print(
                f"Mean           : "
                f"{np.nanmean(aligned)}"
            )

            # --------------------------------------------------
            # Mask cleanup
            # --------------------------------------------------

            if is_mask:

                aligned = np.where(
                    np.isfinite(
                        aligned
                    ),
                    (
                        aligned >= 0.5
                    ).astype(
                        np.float32
                    ),
                    0.0
                )

            raster["data"] = aligned

            raster["shape"] = (
                aligned.shape
            )

            raster["crs"] = (
                reference_crs
            )

            raster["transform"] = (
                reference_transform
            )

            return raster

        # ------------------------------------------------------
        # Fallback interpolation
        # ------------------------------------------------------

        print(
            f"⚠ Using interpolation fallback "
            f"for {name}"
        )

        aligned = self._interpolate(
            data,
            ref_shape
        )

        raster["data"] = aligned

        raster["shape"] = (
            aligned.shape
        )

        return raster

    # ==========================================================
    # INTERPOLATION FALLBACK
    # ==========================================================

    def _interpolate(
        self,
        data,
        target_shape
    ):

        data = np.asarray(
            data,
            dtype=np.float32
        )

        if data.ndim != 2:

            return data

        target_rows, target_cols = (
            target_shape
        )

        source_rows, source_cols = (
            data.shape
        )

        if (
            source_rows == target_rows
            and
            source_cols == target_cols
        ):

            return data.copy()

        row_positions = np.linspace(
            0,
            source_rows - 1,
            target_rows
        )

        col_positions = np.linspace(
            0,
            source_cols - 1,
            target_cols
        )

        temp = np.empty(
            (
                target_rows,
                source_cols
            ),
            dtype=np.float32
        )

        source_rows_index = np.arange(
            source_rows
        )

        for col in range(
            source_cols
        ):

            temp[:, col] = np.interp(
                row_positions,
                source_rows_index,
                data[:, col]
            )

        aligned = np.empty(
            (
                target_rows,
                target_cols
            ),
            dtype=np.float32
        )

        source_cols_index = np.arange(
            source_cols
        )

        for row in range(
            target_rows
        ):

            aligned[row, :] = np.interp(
                col_positions,
                source_cols_index,
                temp[row, :]
            )

        return aligned

    # ==========================================================
    # ALIGN ALL
    # ==========================================================

    def align_all(
        self,
        datasets
    ):

        if datasets is None:

            raise ValueError(
                "Datasets cannot be None."
            )

        if "dem" not in datasets:

            raise KeyError(
                "DEM is required as the "
                "alignment reference."
            )

        dem = datasets.get(
            "dem"
        )

        if dem is None:

            raise ValueError(
                "DEM cannot be None."
            )

        self.set_reference(
            dem
        )

        aligned = {}

        for name, raster in (
            datasets.items()
        ):

            if raster is None:

                aligned[name] = None

                continue

            if name == "earthquake":

                aligned[name] = raster

                continue

            if name == "altimetry":

                aligned[name] = raster

                continue

            is_mask = (
                name == "water_mask"
                or
                name == "flood_mask"
            )

            if isinstance(
                raster,
                dict
            ):

                raster["name"] = name

            aligned[name] = self.align(
                raster,
                is_mask=is_mask,
                name=name
            )

        return aligned