"""
engine.py

Main Tsunami Simulation Engine.

Responsibilities
----------------
- Validate simulation inputs
- Build a localized earthquake source
- Propagate tsunami waves
- Calculate travel time
- Calculate inundation
- Estimate runup
- Calculate hazard
- Return SimulationResult
"""

from __future__ import annotations

import time
from datetime import datetime

import numpy as np

from src.simulation.models import (
    Earthquake,
    WaveResult,
    InundationResult,
    HazardResult,
    RunupResult,
    SimulationResult,
)

from src.simulation.physics import (
    EarthquakeModel,
    WaveModel,
    InundationModel,
    RunupModel,
    HazardModel,
)

from src.simulation.algorithms import (
    WavePropagation,
    WaveAttenuation,
)


class SimulationEngine:

    def __init__(self):

        self.version = "2.1"
        self.last_result = None

    # ==========================================================
    # RUN
    # ==========================================================

    def run(
        self,
        earthquake: Earthquake,
        dem: np.ndarray,
        bathymetry: np.ndarray,
        dem_transform=None
    ) -> SimulationResult:

        start = time.perf_counter()

        self._validate_inputs(
            earthquake,
            dem,
            bathymetry
        )

        dem = np.asarray(
            dem,
            dtype=float
        )

        bathymetry = np.asarray(
            bathymetry,
            dtype=float
        )

        dem = np.where(
            np.isfinite(dem),
            dem,
            0.0
        )

        bathymetry = np.where(
            np.isfinite(bathymetry),
            bathymetry,
            0.0
        )

        # ------------------------------------------------------
        # Earthquake source amplitude
        # ------------------------------------------------------

        source_amplitude = (
            EarthquakeModel.source_amplitude(
                earthquake.magnitude,
                earthquake.slip or 1.0
            )
        )

        rows, cols = bathymetry.shape

        yy, xx = np.indices(
            (rows, cols),
            dtype=float
        )

        # ------------------------------------------------------
        # Locate earthquake source
        # ------------------------------------------------------

        source_y, source_x = (
            self._earthquake_pixel(
                earthquake,
                dem_transform,
                rows,
                cols
            )
        )

        print(
            "\n========== SIMULATION SOURCE =========="
        )

        print(
            "Earthquake latitude :",
            earthquake.latitude
        )

        print(
            "Earthquake longitude:",
            earthquake.longitude
        )

        print(
            "Source pixel row    :",
            source_y
        )

        print(
            "Source pixel column :",
            source_x
        )

        print(
            "Raster centre row   :",
            (rows - 1) / 2.0
        )

        print(
            "Raster centre col   :",
            (cols - 1) / 2.0
        )

        print(
            "========================================"
        )

        # ------------------------------------------------------
        # Pixel dimensions
        # ------------------------------------------------------

        cell_x, cell_y = (
            self._cell_size_metres(
                dem_transform,
                earthquake.latitude
            )
        )

        print(
            "Cell size X (m):",
            cell_x
        )

        print(
            "Cell size Y (m):",
            cell_y
        )

        # ------------------------------------------------------
        # Physical distance from earthquake
        # ------------------------------------------------------

        distance = np.sqrt(

            (
                (xx - source_x)
                * cell_x
            ) ** 2

            +

            (
                (yy - source_y)
                * cell_y
            ) ** 2
        )

        # ------------------------------------------------------
        # Localized tsunami source
        # ------------------------------------------------------

        # FIX: this was 500.0 (metres), giving a real-world
        # Gaussian sigma of ~500 m. That crushed the wave field
        # to ~1e-19 within ~4.6 km of the source, BEFORE
        # radial_decay/exponential/apply_travel_time ever ran on
        # it -- so the far-field attenuation tuning below never
        # mattered; the field was already numerically dead well
        # inside the source-to-coast distance. gaussian_source
        # should only shape the *initial rupture zone*, not the
        # whole propagation; widened so it no longer dominates
        # over the tens-of-km scale this domain needs, leaving
        # radial_decay/exponential/apply_travel_time as the
        # functions actually responsible for far-field decay.
        source_sigma = max(
            150000.0 / min(
                cell_x,
                cell_y
            ),
            5.0
        )

        source = (
            WavePropagation.gaussian_source(
                bathymetry.shape,
                amplitude=source_amplitude,
                sigma=source_sigma,
                center=(
                    source_y,
                    source_x
                )
            )
        )

        # ------------------------------------------------------
        # Water depth
        # ------------------------------------------------------

        water_depth = np.maximum(
            np.abs(bathymetry),
            1.0
        )

        # ------------------------------------------------------
        # Wave speed
        # ------------------------------------------------------

        wave_speed = WaveModel.wave_speed(
            water_depth
        )

        # ------------------------------------------------------
        # Travel time
        # ------------------------------------------------------

        travel_time = WaveModel.travel_time(
            distance,
            water_depth
        )

        # ------------------------------------------------------
        # Radial propagation
        # ------------------------------------------------------

        # FIX: widened from 5,000 m. That length scale crushed
        # the wave within a few km; this domain's real source-to
        # -coast distance is tens of km (~45 km for Palu Bay).
        propagated = (
            WavePropagation.radial_decay(
                source,
                distance,
                attenuation_factor=200000.0
            )
        )

        # ------------------------------------------------------
        # Exponential attenuation
        # ------------------------------------------------------

        # FIX: lowered from 0.0001 so decay length (~1/alpha)
        # is ~200 km instead of ~10 km.
        propagated = (
            WaveAttenuation.exponential(
                propagated,
                distance,
                alpha=0.000005
            )
        )

        # ------------------------------------------------------
        # Travel-time attenuation
        # ------------------------------------------------------

        # FIX: damping lowered from 0.0005 and travel_time is now
        # clipped at 10,800s (3h) inside apply_travel_time, so a
        # shallow/clamped-depth pixel can no longer underflow the
        # whole array via an unbounded exp(-damping * huge_time).
        propagated = (
            WavePropagation.apply_travel_time(
                propagated,
                travel_time,
                damping=0.00002,
                max_travel_time=10800.0
            )
        )

        # ------------------------------------------------------
        # Shoaling
        # ------------------------------------------------------

        shoaling = WaveModel.shoaling_factor(
            water_depth
        )

        propagated = (
            propagated *
            shoaling
        )

        # ------------------------------------------------------
        # Physical limits
        # ------------------------------------------------------

        propagated = WavePropagation.clip(
            propagated,
            minimum=0.0,
            maximum=100.0
        )

        # ------------------------------------------------------
        # Inundation
        # ------------------------------------------------------

        flood_depth = (
            InundationModel.flood_depth(
                propagated,
                dem
            )
        )

        flood_depth = (
            InundationModel.limit_to_land(
                flood_depth,
                dem
            )
        )

        inundation_mask = (
            InundationModel.inundation_mask(
                flood_depth,
                threshold=0.05
            )
        )

        # ------------------------------------------------------
        # Terrain slope
        # ------------------------------------------------------

        gx, gy = np.gradient(
            dem
        )

        slope = np.sqrt(
            gx ** 2 +
            gy ** 2
        )

        slope = np.nan_to_num(
            slope,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

        # ------------------------------------------------------
        # Runup
        # ------------------------------------------------------

        runup = RunupModel.estimate(
            propagated,
            slope
        )

        # ------------------------------------------------------
        # Hazard
        # ------------------------------------------------------

        hazard = HazardModel.hazard_index(
            propagated,
            flood_depth,
            runup
        )

        # ------------------------------------------------------
        # Flood statistics
        # ------------------------------------------------------

        flooded_pixels = int(
            inundation_mask.sum()
        )

        flooded_area_km2 = (
            flooded_pixels
            *
            (
                cell_x
                *
                cell_y
            )
            /
            1_000_000.0
        )

        # ------------------------------------------------------
        # Wave result
        # ------------------------------------------------------

        wave_result = WaveResult(

            wave_height=propagated,

            travel_time=travel_time,

            velocity=wave_speed,

            max_height=float(
                propagated.max()
            ),

            average_height=float(
                propagated.mean()
            ),

            propagation_time=float(
                travel_time.max()
            ),
        )

        # ------------------------------------------------------
        # Inundation result
        # ------------------------------------------------------

        inundation_result = InundationResult(

            flood_depth=flood_depth,

            inundation_mask=inundation_mask,

            flooded_area_km2=float(
                flooded_area_km2
            ),

            maximum_depth=float(
                flood_depth.max()
            ),

            mean_depth=float(
                flood_depth.mean()
            ),
        )

        # ------------------------------------------------------
        # Runup result
        # ------------------------------------------------------

        runup_result = RunupResult(

            runup_height=runup,

            shoreline_height=runup,

            maximum_runup=float(
                runup.max()
            ),

            average_runup=float(
                runup.mean()
            ),

            coastal_length=float(
                np.count_nonzero(
                    dem <= 2.0
                )
            ),
        )

        # ------------------------------------------------------
        # Hazard result
        # ------------------------------------------------------

        hazard_result = HazardResult(

            hazard_map=hazard,

            risk_score=hazard,

            evacuation_time=np.where(
                hazard > 5.0,
                5,
                15
            ),

            highest_risk=float(
                hazard.max()
            ),

            average_risk=float(
                hazard.mean()
            ),
        )

        # ------------------------------------------------------
        # Result
        # ------------------------------------------------------

        end = time.perf_counter()

        result = SimulationResult(

            earthquake=earthquake,

            wave=wave_result,

            inundation=inundation_result,

            hazard=hazard_result,

            runup=runup_result,

            execution_time=(
                end - start
            ),

            created_at=datetime.now(),

            engine_version=self.version,

            successful=True,
        )

        self.last_result = result

        return result

    # ==========================================================
    # EARTHQUAKE PIXEL
    # ==========================================================

    def _earthquake_pixel(
        self,
        earthquake,
        transform,
        rows,
        cols
    ):

        # ------------------------------------------------------
        # Without spatial transform, retain safe centre fallback
        # ------------------------------------------------------

        if transform is None:

            print(
                "⚠ DEM transform unavailable. "
                "Using raster centre as source."
            )

            return (
                (rows - 1) / 2.0,
                (cols - 1) / 2.0
            )

        try:

            col, row = (
                ~transform
                *
                (
                    earthquake.longitude,
                    earthquake.latitude
                )
            )

            print(
                "Geospatial source position:",
                f"row={row:.2f}",
                f"col={col:.2f}"
            )

            return (
                float(row),
                float(col)
            )

        except Exception as exc:

            print(
                "⚠ Could not convert earthquake "
                f"coordinates to raster pixel: {exc}"
            )

            return (
                (rows - 1) / 2.0,
                (cols - 1) / 2.0
            )

    # ==========================================================
    # CELL SIZE
    # ==========================================================

    def _cell_size_metres(
        self,
        transform,
        latitude
    ):

        if transform is None:

            return (
                30.0,
                30.0
            )

        try:

            degrees_x = abs(
                float(
                    transform.a
                )
            )

            degrees_y = abs(
                float(
                    transform.e
                )
            )

            metres_per_degree_lat = 111320.0

            metres_per_degree_lon = (
                111320.0
                *
                np.cos(
                    np.deg2rad(
                        latitude
                    )
                )
            )

            cell_x = (
                degrees_x
                *
                metres_per_degree_lon
            )

            cell_y = (
                degrees_y
                *
                metres_per_degree_lat
            )

            if (
                cell_x <= 0
                or
                cell_y <= 0
            ):

                return (
                    30.0,
                    30.0
                )

            return (
                cell_x,
                cell_y
            )

        except Exception:

            return (
                30.0,
                30.0
            )

    # ==========================================================
    # VALIDATION
    # ==========================================================

    def _validate_inputs(
        self,
        earthquake,
        dem,
        bathymetry
    ):

        if earthquake is None:

            raise ValueError(
                "Earthquake cannot be None."
            )

        if not isinstance(
            dem,
            np.ndarray
        ):

            raise TypeError(
                "DEM must be numpy.ndarray."
            )

        if not isinstance(
            bathymetry,
            np.ndarray
        ):

            raise TypeError(
                "Bathymetry must be numpy.ndarray."
            )

        if dem.ndim != 2:

            raise ValueError(
                "DEM must be a 2D raster."
            )

        if bathymetry.ndim != 2:

            raise ValueError(
                "Bathymetry must be a 2D raster."
            )

        if dem.shape != bathymetry.shape:

            raise ValueError(
                "DEM and Bathymetry dimensions "
                "must match."
            )

        if not np.isfinite(
            dem
        ).any():

            raise ValueError(
                "DEM contains no valid values."
            )

        if not np.isfinite(
            bathymetry
        ).any():

            raise ValueError(
                "Bathymetry contains no valid values."
            )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):

        if self.last_result is None:

            return None

        return self.last_result.summary()

    # ==========================================================
    # REPRESENTATION
    # ==========================================================

    def __repr__(self):

        return (
            f"SimulationEngine("
            f"version={self.version})"
        )