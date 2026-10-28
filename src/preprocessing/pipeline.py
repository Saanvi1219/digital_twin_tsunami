"""
Preprocessing Pipeline

Coordinates all preprocessing loaders and processors.

Inputs:
    - Earthquake GeoJSON
    - DEM
    - Bathymetry
    - Sentinel-2 derived products

Optional:
    - Sentinel-1
    - Altimetry

Sentinel-2 derived products:
    - NDWI_pre.tif
    - NDWI_post.tif
    - NDWI_diff.tif
    - flood_mask.tif
"""

from pathlib import Path
import numpy as np

from src.preprocessing.loaders import (
    EarthquakeLoader,
    DEMLoader,
    BathymetryLoader,
    Sentinel1Loader,
    Sentinel2Loader,
    AltimetryLoader,
)

from src.preprocessing.processors.validator import DatasetValidator
from src.preprocessing.processors.alignment import RasterAlignment
from src.preprocessing.processors.cropping import RasterCropper
from src.preprocessing.processors.normalization import RasterNormalizer


class PreprocessingPipeline:

    def __init__(self):

        self.eq_loader = EarthquakeLoader()
        self.dem_loader = DEMLoader()
        self.bathy_loader = BathymetryLoader()
        self.s1_loader = Sentinel1Loader()
        self.s2_loader = Sentinel2Loader()
        self.alt_loader = AltimetryLoader()

        self.validator = DatasetValidator()
        self.aligner = RasterAlignment()
        self.cropper = RasterCropper()
        self.normalizer = RasterNormalizer()

    # ==========================================================
    # OPTIONAL RASTER LOADER
    # ==========================================================

    def _load_optional_raster(self, filename):

        if filename is None:
            return None

        path = Path(filename)

        if not path.exists():
            print(f"⚠ Optional dataset not found: {path}")
            return None

        try:

            return self.s2_loader.preprocess(
                str(path)
            )

        except Exception as exc:

            print(
                f"⚠ Optional raster could not be loaded: {path}"
            )

            print(
                f"  Reason: {exc}"
            )

            return None

    # ==========================================================
    # SENTINEL-2 DERIVED PRODUCTS
    # ==========================================================

    def _load_sentinel2_products(self, sentinel2_path):

        """
        Loads already-generated Sentinel-2 products.

        Expected directory:

        sentinel2/
            NDWI_pre.tif
            NDWI_post.tif
            NDWI_diff.tif
            flood_mask.tif
        """

        if sentinel2_path is None:

            print("⚠ Sentinel-2 path not supplied.")

            return (
                None,
                None,
                None,
                None,
            )

        path = Path(sentinel2_path)

        # ------------------------------------------------------
        # Directory supplied
        # ------------------------------------------------------

        if path.is_dir():

            # ----------------------------------------------
            # FIX: the old code required exact, case-sensitive
            # filenames ("NDWI_pre.tif" etc). Any real-world
            # naming variation (different case, .tiff extension,
            # underscores/hyphens) silently made the file look
            # "unavailable" even though it existed. This now
            # searches case-insensitively for the first file
            # matching a small set of common patterns.
            # ----------------------------------------------

            def _find_first(patterns):
                for pattern in patterns:
                    matches = sorted(path.glob(pattern))
                    if matches:
                        return matches[0]
                return None

            ndwi_pre_file = _find_first([
                "NDWI_pre.tif", "NDWI_pre.tiff",
                "[Nn][Dd][Ww][Ii]_[Pp][Rr][Ee].tif",
                "[Nn][Dd][Ww][Ii]_[Pp][Rr][Ee].tiff",
                "*ndwi*pre*.tif", "*ndwi*pre*.tiff",
                "*pre*ndwi*.tif", "*pre*ndwi*.tiff",
            ]) or (path / "NDWI_pre.tif")

            ndwi_post_file = _find_first([
                "NDWI_post.tif", "NDWI_post.tiff",
                "[Nn][Dd][Ww][Ii]_[Pp][Oo][Ss][Tt].tif",
                "[Nn][Dd][Ww][Ii]_[Pp][Oo][Ss][Tt].tiff",
                "*ndwi*post*.tif", "*ndwi*post*.tiff",
                "*post*ndwi*.tif", "*post*ndwi*.tiff",
            ]) or (path / "NDWI_post.tif")

            ndwi_diff_file = _find_first([
                "NDWI_diff.tif", "NDWI_diff.tiff",
                "[Nn][Dd][Ww][Ii]_[Dd][Ii][Ff][Ff].tif",
                "[Nn][Dd][Ww][Ii]_[Dd][Ii][Ff][Ff].tiff",
                "*ndwi*diff*.tif", "*ndwi*diff*.tiff",
            ]) or (path / "NDWI_diff.tif")

            flood_mask_file = _find_first([
                "flood_mask.tif", "flood_mask.tiff",
                "[Ff]lood[_-][Mm]ask.tif",
                "[Ff]lood[_-][Mm]ask.tiff",
                "*flood*mask*.tif", "*flood*mask*.tiff",
            ]) or (path / "flood_mask.tif")

            print(
                "[SENTINEL-2] Resolved files -> "
                f"pre={ndwi_pre_file.name if ndwi_pre_file.exists() else 'NOT FOUND'}, "
                f"post={ndwi_post_file.name if ndwi_post_file.exists() else 'NOT FOUND'}, "
                f"diff={ndwi_diff_file.name if ndwi_diff_file.exists() else 'NOT FOUND'}, "
                f"flood_mask={flood_mask_file.name if flood_mask_file.exists() else 'NOT FOUND'}"
            )

        # ------------------------------------------------------
        # Single file supplied
        # ------------------------------------------------------

        else:

            ndwi_pre_file = path
            ndwi_post_file = None
            ndwi_diff_file = None
            flood_mask_file = None

        # ------------------------------------------------------
        # NDWI PRE
        # ------------------------------------------------------

        ndwi_pre = self._load_optional_raster(
            ndwi_pre_file
            if ndwi_pre_file.exists()
            else None
        )

        # ------------------------------------------------------
        # NDWI POST
        # ------------------------------------------------------

        ndwi_post = self._load_optional_raster(
            ndwi_post_file
            if ndwi_post_file is not None
            and ndwi_post_file.exists()
            else None
        )

        # ------------------------------------------------------
        # NDWI DIFFERENCE
        # ------------------------------------------------------

        ndwi_diff = self._load_optional_raster(
            ndwi_diff_file
            if ndwi_diff_file is not None
            and ndwi_diff_file.exists()
            else None
        )

        # ------------------------------------------------------
        # FLOOD MASK
        # ------------------------------------------------------

        flood_mask = self._load_optional_raster(
            flood_mask_file
            if flood_mask_file is not None
            and flood_mask_file.exists()
            else None
        )

        return (
            ndwi_pre,
            ndwi_post,
            ndwi_diff,
            flood_mask,
        )

    # ==========================================================
    # MAIN PIPELINE
    # ==========================================================

    def run(
        self,
        earthquake_file,
        dem_file,
        bathymetry_file,
        sentinel1_file=None,
        sentinel2_file=None,
        altimetry_file=None,
    ):

        print("\n========================================")
        print(" PREPROCESSING PIPELINE")
        print("========================================")

        # ======================================================
        # 1. EARTHQUAKE
        # ======================================================

        print("\n[1/6] Loading earthquake...")

        earthquake = self.eq_loader.preprocess(
            earthquake_file
        )

        print("✓ Earthquake loaded")

        # ======================================================
        # 2. DEM
        # ======================================================

        print("\n[2/6] Loading DEM...")

        dem = self.dem_loader.preprocess(
            dem_file
        )

        print("✓ DEM loaded")

        # ======================================================
        # 3. BATHYMETRY
        # ======================================================

        print("\n[3/6] Loading bathymetry...")

        bathymetry = self.bathy_loader.preprocess(
            bathymetry_file
        )

        print("✓ Bathymetry loaded")

        # ======================================================
        # 4. SENTINEL-1
        # ======================================================

        print("\n[4/6] Loading Sentinel-1...")

        sentinel1 = None

        if sentinel1_file:

            try:

                sentinel1 = self.s1_loader.preprocess(
                    sentinel1_file
                )

                print("✓ Sentinel-1 loaded")

            except Exception as exc:

                print("⚠ Sentinel-1 unavailable.")
                print(f"  Reason: {exc}")

                sentinel1 = None

        else:

            print(
                "⚠ Sentinel-1 skipped "
                "(optional for current run)."
            )

        # ======================================================
        # 5. SENTINEL-2
        # ======================================================

        print(
            "\n[5/6] Loading Sentinel-2 "
            "derived products..."
        )

        (
            ndwi_pre,
            ndwi_post,
            ndwi_diff,
            flood_mask,
        ) = self._load_sentinel2_products(
            sentinel2_file
        )

        if ndwi_pre is not None:
            print("✓ NDWI pre loaded")

        if ndwi_post is not None:
            print("✓ NDWI post loaded")

        if ndwi_diff is not None:
            print("✓ NDWI difference loaded")

        if flood_mask is not None:
            print("✓ Flood mask loaded")

        if (
            ndwi_pre is None
            and ndwi_post is None
            and ndwi_diff is None
            and flood_mask is None
        ):
            print(
                "⚠ No Sentinel-2 derived products available."
            )

        # ======================================================
        # 6. ALTIMETRY
        # ======================================================

        print("\n[6/6] Loading altimetry...")

        altimetry = None

        if altimetry_file:

            try:

                altimetry = self.alt_loader.preprocess(
                    altimetry_file
                )

                print("✓ Altimetry loaded")

            except Exception as exc:

                print("⚠ Altimetry unavailable.")
                print(f"  Reason: {exc}")

                altimetry = None

        else:

            print(
                "⚠ Altimetry skipped "
                "(optional for current run)."
            )

        # ======================================================
        # DATASET COLLECTION
        # ======================================================

        datasets = {
            "earthquake": earthquake,
            "dem": dem,
            "bathymetry": bathymetry,
            "sentinel1": sentinel1,
            "altimetry": altimetry,
            "ndwi_pre": ndwi_pre,
            "ndwi_post": ndwi_post,
            "ndwi_diff": ndwi_diff,
            "water_mask": flood_mask,
        }

        # ======================================================
        # DATASET VALIDATION
        # ======================================================

        print("\nValidating datasets...")

        try:

            self.validator.validate(
                datasets
            )

            print("✓ Validation complete")

        except Exception as exc:

            print(
                "⚠ Dataset validation reported an issue:"
            )

            print(
                f"  {exc}"
            )

        # ======================================================
        # RASTER ALIGNMENT
        # ======================================================

        print("\nAligning raster datasets...")

        try:

            datasets = self.aligner.align_all(
                datasets
            )

            print("✓ Alignment complete")

        except Exception as exc:

            print(
                "⚠ Raster alignment failed:"
            )

            print(
                f"  {exc}"
            )

            raise

        # ======================================================
        # CROPPING
        # ======================================================

        print("\nCropping datasets...")

        try:

            datasets = self.cropper.crop_all(
                datasets
            )

            print("✓ Cropping complete")

        except Exception as exc:

            print(
                "⚠ Raster cropping failed:"
            )

            print(
                f"  {exc}"
            )

            raise

        # ======================================================
        # NORMALIZATION
        # ======================================================

        print("\nNormalizing datasets...")

        try:

            datasets = self.normalizer.normalize_all(
                datasets
            )

            print("✓ Normalization complete")

        except Exception as exc:

            print(
                "⚠ Raster normalization failed:"
            )

            print(
                f"  {exc}"
            )

            raise

        # ======================================================
        # PHYSICAL RASTER CHECK
        # ======================================================

        print(
            "\n========== PHYSICAL RASTER CHECK =========="
        )

        dem_dataset = datasets.get("dem")

        if (
            isinstance(dem_dataset, dict)
            and dem_dataset.get("data") is not None
        ):

            dem_data = np.asarray(
                dem_dataset["data"],
                dtype=np.float32
            )

            finite_dem = np.isfinite(dem_data)

            if np.any(finite_dem):

                print("DEM physical values:")
                print(
                    "Min   :",
                    float(np.nanmin(dem_data))
                )
                print(
                    "Max   :",
                    float(np.nanmax(dem_data))
                )
                print(
                    "Mean  :",
                    float(np.nanmean(dem_data))
                )
                print(
                    "Shape :",
                    dem_data.shape
                )

            else:

                print(
                    "⚠ DEM contains no finite values."
                )

            if "normalized_data" in dem_dataset:

                dem_normalized = np.asarray(
                    dem_dataset["normalized_data"],
                    dtype=np.float32
                )

                finite_normalized = np.isfinite(
                    dem_normalized
                )

                if np.any(finite_normalized):

                    print(
                        "\nDEM normalized values:"
                    )

                    print(
                        "Min   :",
                        float(
                            np.nanmin(
                                dem_normalized
                            )
                        )
                    )

                    print(
                        "Max   :",
                        float(
                            np.nanmax(
                                dem_normalized
                            )
                        )
                    )

                    print(
                        "Mean  :",
                        float(
                            np.nanmean(
                                dem_normalized
                            )
                        )
                    )

                else:

                    print(
                        "⚠ DEM normalized data "
                        "contains no finite values."
                    )

        else:

            print(
                "⚠ DEM physical data unavailable."
            )

        print(
            "============================================\n"
        )

        # ======================================================
        # STANDARD NDWI FIELD
        # ======================================================

        if datasets.get("ndwi_diff") is not None:

            datasets["ndwi"] = datasets["ndwi_diff"]

            print(
                "✓ NDWI feature set "
                "from NDWI difference"
            )

        elif datasets.get("ndwi_post") is not None:

            datasets["ndwi"] = datasets["ndwi_post"]

            print(
                "✓ NDWI feature set "
                "from NDWI post"
            )

        elif datasets.get("ndwi_pre") is not None:

            datasets["ndwi"] = datasets["ndwi_pre"]

            print(
                "✓ NDWI feature set "
                "from NDWI pre"
            )

        else:

            datasets["ndwi"] = None

            print(
                "⚠ No NDWI product available"
            )

        # ======================================================
        # FINAL DATASET SUMMARY
        # ======================================================

        print(
            "\n========== FINAL DATASET STATUS =========="
        )

        for name, dataset in datasets.items():

            if dataset is None:

                print(
                    f"{name:15} : unavailable"
                )

            elif isinstance(dataset, dict):

                data = dataset.get("data")

                if data is None:

                    print(
                        f"{name:15} : loaded, no data array"
                    )

                else:

                    try:

                        shape = np.asarray(
                            data
                        ).shape

                        print(
                            f"{name:15} : {shape}"
                        )

                    except Exception:

                        print(
                            f"{name:15} : loaded"
                        )

            else:

                print(
                    f"{name:15} : loaded"
                )

        print(
            "============================================"
        )

        print(
            "\n========================================"
        )

        print(
            " PREPROCESSING COMPLETED"
        )

        print(
            "========================================\n"
        )

        return datasets