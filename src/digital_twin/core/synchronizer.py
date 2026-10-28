from __future__ import annotations

from datetime import datetime
from typing import Optional

from src.digital_twin.core.state_manager import StateManager

from src.digital_twin.services.validator import TwinValidator

from src.digital_twin.events.event import (
    Event,
    EventType,
)

from src.digital_twin.events.event_bus import EventBus

class Synchronizer:
    """
    Synchronizes the Digital Twin after every update.

    This class guarantees that dependent data
    remains consistent.
    """

    def __init__(
        self,
        manager: StateManager,
        validator: TwinValidator,
        event_bus: Optional[EventBus] = None
    ):

        self.manager = manager

        self.validator = validator

        self.event_bus = event_bus

        self.last_sync = None

        self.sync_counter = 0

    # ==========================================================

    def synchronize(self):

        """
        Main synchronization routine.
        """

        state = self.manager.state

        self.validator.validate_state(state)

        self.invalidate_if_needed()

        self.last_sync = datetime.utcnow()

        self.sync_counter += 1

        self.publish_sync()

    # ==========================================================

    def invalidate_if_needed(self):

        """
        Remove stale simulation outputs.

        Example

        Earthquake changes

            ↓

        Hazard Map removed

            ↓

        Simulation reruns
        """

        state = self.manager.state

        # DEM missing

        if state.dem is None:

            state.tsunami = None

            state.inundation = None

            state.hazard_map = None

            state.evacuation_map = None

        # Bathymetry missing

        if state.bathymetry is None:

            state.tsunami = None

        # Earthquake missing

        if state.earthquake is None:

            state.tsunami = None

    # ==========================================================

    def publish_sync(self):

        """
        Publish synchronization event.
        """

        if self.event_bus is None:

            return

        event = Event(

            event_type=EventType.STATE_UPDATED,

            source="Synchronizer",

            payload={

                "sync_time":

                    self.last_sync,

                "version":

                    self.manager.state.version

            }

        )

        self.event_bus.publish(event)

    # ==========================================================

    def synchronize_earthquake(self):

        """
        Earthquake updated.
        """

        state = self.manager.state

        state.reset_simulation()

        state.clear_predictions()

        self.synchronize()

    # ==========================================================

    def synchronize_dem(self):

        """
        DEM updated.
        """

        state = self.manager.state

        state.reset_simulation()

        self.synchronize()

    # ==========================================================

    def synchronize_bathymetry(self):

        """
        Bathymetry updated.
        """

        state = self.manager.state

        state.reset_simulation()

        self.synchronize()

    # ==========================================================

    def synchronize_prediction(self):

        """
        AI prediction updated.
        """

        self.synchronize()

    # ==========================================================

    def synchronize_simulation(self):

        """
        Simulation completed.
        """

        self.synchronize()

    # ==========================================================

    def synchronize_everything(self):

        """
        Force complete synchronization.
        """

        self.manager.touch()

        self.synchronize()

    # ==========================================================

    @property
    def synchronized(self):

        return self.last_sync is not None

    # ==========================================================

    def status(self):

        return {

            "synchronized":

                self.synchronized,

            "sync_counter":

                self.sync_counter,

            "last_sync":

                self.last_sync,

            "version":

                self.manager.state.version

        }

    # ==========================================================

    def summary(self):

        print()

        print("========== Synchronizer ==========")

        print(

            "Version:",

            self.manager.state.version

        )

        print(

            "Synchronized:",

            self.synchronized

        )

        print(

            "Sync Count:",

            self.sync_counter

        )

        print(

            "Last Sync:",

            self.last_sync

        )

        print()

    # ==========================================================

    def reset(self):

        self.sync_counter = 0

        self.last_sync = None

    # ==========================================================

    def __repr__(self):

        return (

            f"Synchronizer("

            f"syncs={self.sync_counter})"

        )
        