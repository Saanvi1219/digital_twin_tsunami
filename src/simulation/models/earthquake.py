"""
earthquake.py

Earthquake source model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Earthquake:

    event: str

    latitude: float

    longitude: float

    depth: float

    magnitude: float

    origin_time: Optional[datetime] = None

    strike: Optional[float] = None

    dip: Optional[float] = None

    rake: Optional[float] = None

    fault_length: Optional[float] = None

    fault_width: Optional[float] = None

    slip: Optional[float] = None

    def epicenter(self):

        return (

            self.latitude,

            self.longitude

        )

    @property
    def moment_magnitude(self):

        return self.magnitude

    def __str__(self):

        return (

            f"M{self.magnitude} "

            f"Earthquake "

            f"({self.latitude}, {self.longitude})"

        )