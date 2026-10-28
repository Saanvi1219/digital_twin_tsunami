from __future__ import annotations

from typing import Any, Dict, List

import numpy as np

from src.digital_twin.models.dt_state import TwinState
from src.digital_twin.exceptions import ValidationError


class TwinValidator:
    """
    Performs validation on Digital Twin data.

    Responsibilities
    ----------------
    - Validate earthquake parameters
    - Validate DEM
    - Validate bathymetry
    - Validate satellite imagery
    - Validate metadata
    - Validate coordinates
    """

    def __init__(self):

        self.errors: List[str] = []
        self.warnings: List[str] = []

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.errors.clear()
        self.warnings.clear()

    # ==================================================
    # COMPLETE STATE VALIDATION
    # ==================================================

    def validate_state(
        self,
        state: TwinState
    ) -> bool:

        self.reset()

        self.validate_version(state)
        self.validate_metadata(state)
        self.validate_earthquake(state)
        self.validate_dem(state)
        self.validate_bathymetry(state)
        self.validate_prediction(state)

        return len(self.errors) == 0

    # ==================================================
    # VERSION
    # ==================================================

    def validate_version(
        self,
        state: TwinState
    ):

        if state.version < 1:

            self.errors.append(
                "Version number cannot be less than 1."
            )

    # ==================================================
    # METADATA
    # ==================================================

    def validate_metadata(
        self,
        state: TwinState
    ):

        if not isinstance(
            state.metadata,
            dict
        ):

            self.errors.append(
                "Metadata must be a dictionary."
            )

    # ==================================================
    # PREDICTION / CONFIDENCE
    # ==================================================

    def validate_prediction(
        self,
        state: TwinState
    ):

        if state.confidence is not None:

            try:

                confidence = float(
                    state.confidence
                )

                if not 0 <= confidence <= 1:

                    self.errors.append(
                        "Confidence must lie between 0 and 1."
                    )

            except (
                TypeError,
                ValueError
            ):

                self.errors.append(
                    "Confidence must be numeric."
                )

    # ==================================================
    # EARTHQUAKE
    # ==================================================

    def validate_earthquake(
        self,
        state: TwinState
    ):

        # ------------------------------------------------
        # Missing earthquake
        # ------------------------------------------------

        if state.earthquake is None:

            self.warnings.append(
                "Earthquake data not loaded."
            )

            return

        eq = state.earthquake

        required = [
            "latitude",
            "longitude",
            "depth",
            "magnitude",
        ]

        # ------------------------------------------------
        # Support BOTH:
        #
        # 1. Dictionary
        # 2. Earthquake dataclass/object
        # ------------------------------------------------

        if isinstance(eq, dict):

            for field in required:

                if field not in eq:

                    self.errors.append(
                        f"Missing earthquake field: {field}"
                    )

            # --------------------------------------------
            # Magnitude
            # --------------------------------------------

            if "magnitude" in eq:

                mag = eq["magnitude"]

                self._validate_magnitude(
                    mag
                )

            # --------------------------------------------
            # Depth
            # --------------------------------------------

            if "depth" in eq:

                depth = eq["depth"]

                self._validate_depth(
                    depth
                )

            return

        # ------------------------------------------------
        # Object / Dataclass
        # ------------------------------------------------

        for field in required:

            if not hasattr(eq, field):

                self.errors.append(
                    f"Missing earthquake field: {field}"
                )

        # ------------------------------------------------
        # Magnitude
        # ------------------------------------------------

        if hasattr(
            eq,
            "magnitude"
        ):

            mag = getattr(
                eq,
                "magnitude"
            )

            self._validate_magnitude(
                mag
            )

        # ------------------------------------------------
        # Depth
        # ------------------------------------------------

        if hasattr(
            eq,
            "depth"
        ):

            depth = getattr(
                eq,
                "depth"
            )

            self._validate_depth(
                depth
            )

    # ==================================================
    # MAGNITUDE VALIDATION
    # ==================================================

    def _validate_magnitude(
        self,
        magnitude
    ):

        if magnitude is None:

            self.errors.append(
                "Earthquake magnitude is missing."
            )

            return

        try:

            magnitude = float(
                magnitude
            )

        except (
            TypeError,
            ValueError
        ):

            self.errors.append(
                "Earthquake magnitude must be numeric."
            )

            return

        if magnitude < 0 or magnitude > 10:

            self.errors.append(
                "Magnitude outside valid range."
            )

    # ==================================================
    # DEPTH VALIDATION
    # ==================================================

    def _validate_depth(
        self,
        depth
    ):

        if depth is None:

            self.errors.append(
                "Earthquake depth is missing."
            )

            return

        try:

            depth = float(
                depth
            )

        except (
            TypeError,
            ValueError
        ):

            self.errors.append(
                "Earthquake depth must be numeric."
            )

            return

        if depth < 0:

            self.errors.append(
                "Depth cannot be negative."
            )

    # ==================================================
    # DEM
    # ==================================================

    def validate_dem(
        self,
        state: TwinState
    ):

        if state.dem is None:

            self.warnings.append(
                "DEM missing."
            )

            return

        if not isinstance(
            state.dem,
            np.ndarray
        ):

            self.errors.append(
                "DEM must be numpy array."
            )

            return

        if state.dem.size == 0:

            self.errors.append(
                "DEM is empty."
            )

    # ==================================================
    # BATHYMETRY
    # ==================================================

    def validate_bathymetry(
        self,
        state: TwinState
    ):

        if state.bathymetry is None:

            self.warnings.append(
                "Bathymetry missing."
            )

            return

        if not isinstance(
            state.bathymetry,
            np.ndarray
        ):

            self.errors.append(
                "Bathymetry must be numpy array."
            )

            return

        if state.bathymetry.size == 0:

            self.errors.append(
                "Bathymetry is empty."
            )

    # ==================================================
    # VALIDATION REPORT
    # ==================================================

    def validation_report(
        self
    ) -> Dict[str, Any]:

        return {

            "valid":
                len(self.errors) == 0,

            "errors":
                self.errors,

            "warnings":
                self.warnings,

            "error_count":
                len(self.errors),

            "warning_count":
                len(self.warnings),

        }

    # ==================================================
    # RAISE IF INVALID
    # ==================================================

    def raise_if_invalid(self):

        if self.errors:

            raise ValidationError(
                "\n".join(
                    self.errors
                )
            )