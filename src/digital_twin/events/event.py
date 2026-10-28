"""
event.py
~~~~~~~~

Core event definitions for the Digital Twin framework.

Every significant action inside the Digital Twin is represented as
an Event object.

Examples
--------
- EarthquakeLoaded
- DEMLoaded
- SimulationStarted
- SimulationCompleted
- StateUpdated
- SnapshotCreated
- RollbackPerformed

Author
------
Digital Twin Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field

from datetime import datetime

from enum import Enum

from typing import Any, Dict

import uuid


# ============================================================
# Event Types
# ============================================================

class EventType(Enum):
    """
    Enumeration of all supported event types.
    """

    INITIALIZED = "initialized"

    STATE_UPDATED = "state_updated"

    EARTHQUAKE_LOADED = "earthquake_loaded"

    DEM_LOADED = "dem_loaded"

    BATHYMETRY_LOADED = "bathymetry_loaded"

    SATELLITE_LOADED = "satellite_loaded"

    SNAPSHOT_CREATED = "snapshot_created"

    VERSION_CREATED = "version_created"

    VALIDATION_COMPLETED = "validation_completed"

    SIMULATION_STARTED = "simulation_started"

    SIMULATION_COMPLETED = "simulation_completed"

    SIMULATION_FAILED = "simulation_failed"

    ROLLBACK = "rollback"

    SERIALIZED = "serialized"

    DESERIALIZED = "deserialized"

    ERROR = "error"

    WARNING = "warning"


# ============================================================
# Base Event
# ============================================================

@dataclass(slots=True)
class Event:
    """
    Base Event class.

    Every event published inside the Digital Twin
    inherits from this object.
    """

    event_type: EventType

    source: str

    payload: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    priority: int = 0

    handled: bool = False

    # -------------------------------------------------------

    def mark_handled(self):

        """
        Mark the event as processed.
        """

        self.handled = True

    # -------------------------------------------------------

    def add_payload(

        self,

        key: str,

        value: Any

    ):

        """
        Add data to payload.
        """

        self.payload[key] = value

    # -------------------------------------------------------

    def get(

        self,

        key,

        default=None

    ):

        return self.payload.get(

            key,

            default

        )

    # -------------------------------------------------------

    @property
    def age_seconds(self):

        """
        Seconds since creation.
        """

        return (

            datetime.utcnow()

            - self.timestamp

        ).total_seconds()

    # -------------------------------------------------------

    def to_dict(self):

        return {

            "event_id": self.event_id,

            "event_type": self.event_type.value,

            "source": self.source,

            "timestamp": self.timestamp.isoformat(),

            "payload": self.payload,

            "priority": self.priority,

            "handled": self.handled

        }

    # -------------------------------------------------------

    def __repr__(self):

        return (

            f"Event("

            f"{self.event_type.value}, "

            f"id={self.event_id[:8]}, "

            f"source={self.source})"

        )


# ============================================================
# Factory Functions
# ============================================================

def create_state_update_event(
    source: str,
    payload: Dict[str, Any]
) -> Event:
    """
    Create a state update event.
    """

    return Event(

        event_type=EventType.STATE_UPDATED,

        source=source,

        payload=payload

    )


def create_simulation_started_event(
    source: str
) -> Event:

    return Event(

        event_type=EventType.SIMULATION_STARTED,

        source=source

    )


def create_simulation_completed_event(
    source: str,
    results: Dict[str, Any]
) -> Event:

    return Event(

        event_type=EventType.SIMULATION_COMPLETED,

        source=source,

        payload=results

    )


def create_error_event(
    source: str,
    message: str
) -> Event:

    return Event(

        event_type=EventType.ERROR,

        source=source,

        payload={

            "message": message

        }

    )


def create_snapshot_event(
    source: str,
    version: int
) -> Event:

    return Event(

        event_type=EventType.SNAPSHOT_CREATED,

        source=source,

        payload={

            "version": version

        }

    )