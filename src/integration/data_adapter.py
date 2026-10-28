"""
Data Adapter

Converts preprocessing outputs into TsunamiFeatures.

Raster dictionaries are converted into their physical
numpy arrays before being passed to the simulation engine.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np

from src.simulation.models import Earthquake


@dataclass(slots=True)
class TsunamiFeatures:

    earthquake: Earthquake

    dem: Any
    bathymetry: Any

    sentinel1: Any = None
    sentinel2: Any = None
    altimetry: Any = None

    ndwi: Any = None
    water_mask: Any = None

    mean_elevation: float = 0.0
    max_elevation: float = 0.0
    min_elevation: float = 0.0

    mean_bathymetry: float = 0.0

    mean_ndwi: float = 0.0

    inundation_area: float = 0.0

    ground_deformation: float = 0.0

    dem_transform: Any = None
    bathymetry_transform: Any = None


class DataAdapter:

    # ==========================================================
    # EXTRACT ARRAY
    # ==========================================================

    @staticmethod
    def _array(dataset):

        if dataset is None:
            return None

        if isinstance(
            dataset,
            dict
        ):

            data = dataset.get(
                "data"
            )

            if data is None:
                return None

            return np.asarray(
                data,
                dtype=np.float32
            )

        try:

            return np.asarray(
                dataset,
                dtype=np.float32
            )

        except Exception:

            return None

    # ==========================================================
    # EXTRACT TRANSFORM
    # ==========================================================

    @staticmethod
    def _transform(dataset):

        if not isinstance(
            dataset,
            dict
        ):

            return None

        return dataset.get(
            "transform"
        )

    # ==========================================================
    # SAFE MEAN
    # ==========================================================

    @staticmethod
    def _safe_mean(array):

        array = DataAdapter._array(
            array
        )

        if array is None:
            return 0.0

        finite = np.isfinite(
            array
        )

        if not np.any(finite):
            return 0.0

        return float(
            np.nanmean(
                array
            )
        )

    # ==========================================================
    # SAFE MAX
    # ==========================================================

    @staticmethod
    def _safe_max(array):

        array = DataAdapter._array(
            array
        )

        if array is None:
            return 0.0

        finite = np.isfinite(
            array
        )

        if not np.any(finite):
            return 0.0

        return float(
            np.nanmax(
                array
            )
        )

    # ==========================================================
    # SAFE MIN
    # ==========================================================

    @staticmethod
    def _safe_min(array):

        array = DataAdapter._array(
            array
        )

        if array is None:
            return 0.0

        finite = np.isfinite(
            array
        )

        if not np.any(finite):
            return 0.0

        return float(
            np.nanmin(
                array
            )
        )

    # ==========================================================
    # SAFE SUM
    # ==========================================================

    @staticmethod
    def _safe_sum(array):

        array = DataAdapter._array(
            array
        )

        if array is None:
            return 0.0

        return float(
            np.nansum(
                array
            )
        )

    # ==========================================================
    # ADAPT
    # ==========================================================

    def adapt(
        self,
        datasets
    ):

        if datasets is None:

            raise ValueError(
                "Datasets cannot be None."
            )

        # ------------------------------------------------------
        # Earthquake
        # ------------------------------------------------------

        earthquake_data = (
            datasets.get(
                "earthquake",
                {}
            )
        )

        if not isinstance(
            earthquake_data,
            dict
        ):

            earthquake_data = {}

        earthquake = Earthquake(

            event=earthquake_data.get(
                "event",
                "Unknown"
            ),

            latitude=float(
                earthquake_data.get(
                    "latitude",
                    0.0
                )
            ),

            longitude=float(
                earthquake_data.get(
                    "longitude",
                    0.0
                )
            ),

            depth=float(
                earthquake_data.get(
                    "depth",
                    0.0
                )
            ),

            magnitude=float(
                earthquake_data.get(
                    "magnitude",
                    0.0
                )
            ),

            origin_time=earthquake_data.get(
                "origin_time"
            ),

            strike=earthquake_data.get(
                "strike"
            ),

            dip=earthquake_data.get(
                "dip"
            ),

            rake=earthquake_data.get(
                "rake"
            ),

            fault_length=earthquake_data.get(
                "fault_length"
            ),

            fault_width=earthquake_data.get(
                "fault_width"
            ),

            slip=earthquake_data.get(
                "slip"
            ),
        )

        # ------------------------------------------------------
        # Physical raster arrays
        # ------------------------------------------------------

        dem = self._array(
            datasets.get(
                "dem"
            )
        )

        bathymetry = self._array(
            datasets.get(
                "bathymetry"
            )
        )

        sentinel1 = self._array(
            datasets.get(
                "sentinel1"
            )
        )

        sentinel2 = self._array(
            datasets.get(
                "sentinel2"
            )
        )

        altimetry = self._array(
            datasets.get(
                "altimetry"
            )
        )

        ndwi = self._array(
            datasets.get(
                "ndwi"
            )
        )

        water_mask = self._array(
            datasets.get(
                "water_mask"
            )
        )

        # ------------------------------------------------------
        # Spatial metadata
        # ------------------------------------------------------

        dem_transform = self._transform(
            datasets.get(
                "dem"
            )
        )

        bathymetry_transform = self._transform(
            datasets.get(
                "bathymetry"
            )
        )

        # ------------------------------------------------------
        # Build features
        # ------------------------------------------------------

        features = TsunamiFeatures(

            earthquake=earthquake,

            dem=dem,

            bathymetry=bathymetry,

            sentinel1=sentinel1,

            sentinel2=sentinel2,

            altimetry=altimetry,

            ndwi=ndwi,

            water_mask=water_mask,

            mean_elevation=self._safe_mean(
                dem
            ),

            max_elevation=self._safe_max(
                dem
            ),

            min_elevation=self._safe_min(
                dem
            ),

            mean_bathymetry=self._safe_mean(
                bathymetry
            ),

            mean_ndwi=self._safe_mean(
                ndwi
            ),

            inundation_area=self._safe_sum(
                water_mask
            ),

            ground_deformation=float(
                earthquake_data.get(
                    "ground_deformation",
                    datasets.get(
                        "ground_deformation",
                        0.0
                    )
                )
            ),

            dem_transform=dem_transform,

            bathymetry_transform=(
                bathymetry_transform
            ),
        )

        # ------------------------------------------------------
        # Diagnostics
        # ------------------------------------------------------

        print(
            "\n========== DATA ADAPTER CHECK =========="
        )

        if dem is not None:

            print(
                "DEM:",
                dem.shape,
                "min=",
                float(np.nanmin(dem)),
                "max=",
                float(np.nanmax(dem)),
                "mean=",
                float(np.nanmean(dem))
            )

        else:

            print(
                "DEM: unavailable"
            )

        if bathymetry is not None:

            print(
                "Bathymetry:",
                bathymetry.shape,
                "min=",
                float(np.nanmin(bathymetry)),
                "max=",
                float(np.nanmax(bathymetry)),
                "mean=",
                float(np.nanmean(bathymetry))
            )

        else:

            print(
                "Bathymetry: unavailable"
            )

        if water_mask is not None:

            print(
                "Observed flood pixels:",
                int(
                    np.sum(
                        water_mask > 0.5
                    )
                )
            )

        else:

            print(
                "Observed flood mask: unavailable"
            )

        print(
            "Earthquake latitude:",
            earthquake.latitude
        )

        print(
            "Earthquake longitude:",
            earthquake.longitude
        )

        print(
            "DEM transform available:",
            dem_transform is not None
        )

        print(
            "========================================\n"
        )

        return features