"""
Digital Twin State

Stores the complete synchronized state of the tsunami digital twin.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(slots=True)
class TwinState:
    """
    Represents one complete state of the Digital Twin.

    Every dataset loaded into the project eventually becomes
    part of this object.
    """

    # ----------------------------
    # Raw Inputs
    # ----------------------------

    earthquake: Optional[Any] = None
    dem: Optional[Any] = None
    bathymetry: Optional[Any] = None
    sentinel1: Optional[Any] = None
    sentinel2: Optional[Any] = None
    altimetry: Optional[Any] = None
    simulation_result: object = None

    # ----------------------------
    # Simulation Outputs
    # ----------------------------

    tsunami: Optional[Any] = None
    inundation: Optional[Any] = None
    hazard_map: Optional[Any] = None
    evacuation_map: Optional[Any] = None

    # ----------------------------
    # AI Outputs
    # ----------------------------

    prediction: Optional[Any] = None
    confidence: Optional[float] = None

    # ----------------------------
    # Metadata
    # ----------------------------

    version: int = 1

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    notes: str = ""

    author: str = "Digital Twin Engine"

    project: str = "Sulawesi 2018 Tsunami"

    scenario: str = "Default"

    # -----------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert TwinState into a serializable dictionary.
        """

        return {

            "earthquake": self.earthquake,
            "dem": self.dem,
            "bathymetry": self.bathymetry,
            "sentinel1": self.sentinel1,
            "sentinel2": self.sentinel2,
            "altimetry": self.altimetry,

            "tsunami": self.tsunami,
            "inundation": self.inundation,
            "hazard_map": self.hazard_map,
            "evacuation_map": self.evacuation_map,

            "prediction": self.prediction,
            "confidence": self.confidence,

            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "notes": self.notes,
            "author": self.author,
            "project": self.project,
            "scenario": self.scenario,
        }

    # -----------------------------------

    def increment_version(self) -> None:

        self.version += 1

        self.timestamp = datetime.utcnow()

    # -----------------------------------

    def clear_predictions(self):

        self.prediction = None

        self.confidence = None

    # -----------------------------------

    def reset_simulation(self):

        self.tsunami = None

        self.inundation = None

        self.hazard_map = None

        self.evacuation_map = None

    # -----------------------------------

    @property
    def is_ready(self):

        return (

            self.earthquake is not None
            and self.dem is not None

        )