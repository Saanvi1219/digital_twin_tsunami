"""
==================================================
Earthquake Data Model
==================================================
"""

from dataclasses import dataclass


@dataclass
class EarthquakeData:
    """
    Stores earthquake information.
    """

    event_id: str

    place: str

    magnitude: float

    time: int

    latitude: float

    longitude: float

    depth: float

    status: str

    tsunami: int