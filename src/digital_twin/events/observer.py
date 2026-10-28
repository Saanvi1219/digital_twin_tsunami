"""
observer.py
~~~~~~~~~~~

Observer Pattern implementation for the Digital Twin.

Observers subscribe to events published by the EventBus and react
automatically without tight coupling.

Author
------
Digital Twin Engine
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from .event import Event, EventType


# ============================================================
# Base Observer
# ============================================================

class Observer(ABC):
    """
    Abstract base class for every observer.

    Every observer must implement update().
    """

    def __init__(self, name: str):

        self.name = name

        self.created_at = datetime.utcnow()

        self.enabled = True

        self.event_count = 0

    # ------------------------------------------------------

    @abstractmethod
    def update(self, event: Event) -> None:
        """
        Handle an incoming event.
        """
        pass

    # ------------------------------------------------------

    def enable(self):

        self.enabled = True

    # ------------------------------------------------------

    def disable(self):

        self.enabled = False

    # ------------------------------------------------------

    def reset_counter(self):

        self.event_count = 0

    # ------------------------------------------------------

    def info(self):

        return {

            "name": self.name,

            "enabled": self.enabled,

            "events_processed": self.event_count,

            "created_at": self.created_at.isoformat()

        }

    # ------------------------------------------------------

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(name={self.name})"

        )


# ============================================================
# Logging Observer
# ============================================================

class LoggingObserver(Observer):
    """
    Logs every event received.
    """

    def __init__(self):

        super().__init__("LoggingObserver")

    def update(self, event: Event):

        if not self.enabled:

            return

        self.event_count += 1

        print(

            f"[LOG] "

            f"{event.timestamp} "

            f"{event.event_type.value}"

        )


# ============================================================
# History Observer
# ============================================================

class HistoryObserver(Observer):
    """
    Saves state updates into HistoryManager.
    """

    def __init__(self, history):

        super().__init__("HistoryObserver")

        self.history = history

    def update(self, event: Event):

        if not self.enabled:

            return

        self.event_count += 1

        if (

            event.event_type

            == EventType.STATE_UPDATED

        ):

            state = event.get("state")

            if state is not None:

                self.history.save(

                    state,

                    message="Automatic Snapshot"

                )


# ============================================================
# Version Observer
# ============================================================

class VersionObserver(Observer):
    """
    Automatically commits versions.
    """

    def __init__(self, version_controller):

        super().__init__("VersionObserver")

        self.version_controller = version_controller

    def update(self, event: Event):

        if not self.enabled:

            return

        self.event_count += 1

        if (

            event.event_type

            == EventType.STATE_UPDATED

        ):

            self.version_controller.commit(

                description="State Updated"

            )


# ============================================================
# Validation Observer
# ============================================================

class ValidationObserver(Observer):
    """
    Validates every state update.
    """

    def __init__(self, validator):

        super().__init__("ValidationObserver")

        self.validator = validator

    def update(self, event: Event):

        if not self.enabled:

            return

        self.event_count += 1

        if (

            event.event_type

            == EventType.STATE_UPDATED

        ):

            state = event.get("state")

            if state:

                self.validator.validate_state(

                    state

                )


# ============================================================
# Metrics Observer
# ============================================================

class MetricsObserver(Observer):
    """
    Tracks statistics.
    """

    def __init__(self):

        super().__init__("MetricsObserver")

        self.total_events = 0

        self.errors = 0

        self.warnings = 0

    def update(self, event: Event):

        if not self.enabled:

            return

        self.total_events += 1

        self.event_count += 1

        if event.event_type == EventType.ERROR:

            self.errors += 1

        elif event.event_type == EventType.WARNING:

            self.warnings += 1

    def summary(self):

        return {

            "events": self.total_events,

            "errors": self.errors,

            "warnings": self.warnings

        }


# ============================================================
# Simulation Observer
# ============================================================

class SimulationObserver(Observer):
    """
    Placeholder observer that will trigger the tsunami simulation.
    """

    def __init__(self):

        super().__init__("SimulationObserver")

    def update(self, event: Event):

        if not self.enabled:

            return

        self.event_count += 1

        if (

            event.event_type

            == EventType.SIMULATION_STARTED

        ):

            print(

                "Launching Tsunami Simulation..."

            )