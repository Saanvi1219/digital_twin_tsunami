"""
twin.py
=======

Main Digital Twin class.

This class orchestrates the complete Digital Twin lifecycle.

Responsibilities
----------------
- State Management
- Validation
- Version Control
- Rollback
- History
- Serialization
- Event System
- Synchronization
- Simulation Interface

Author
------
Digital Twin Engine
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional


# Core
from src.digital_twin.core.state_manager import StateManager
from src.digital_twin.core.updater import TwinUpdater
from src.digital_twin.core.synchronizer import Synchronizer


# Models
from src.digital_twin.models.dt_state import TwinState


# Services
from src.digital_twin.services.validator import TwinValidator
from src.digital_twin.services.history import HistoryManager
from src.digital_twin.services.rollback import RollbackManager
from src.digital_twin.services.serializer import TwinSerializer
from src.digital_twin.services.version_control import VersionController


# Events
from src.digital_twin.events.event_bus import EventBus

from src.digital_twin.events.observer import (
    LoggingObserver,
    HistoryObserver,
    VersionObserver,
    ValidationObserver,
    MetricsObserver,
)

from src.digital_twin.events.event import EventType
from src.digital_twin.integration import SimulationAdapter



class DigitalTwin:
    """
    Main Digital Twin object.

    Every interaction with the project should happen
    through this class.
    """

    def __init__(self):

        # ==================================================
        # Event System
        # ==================================================

        self.event_bus = EventBus()

        # ==================================================
        # Services
        # ==================================================

        self.validator = TwinValidator()

        self.history = HistoryManager()

        self.version = VersionController()

        self.serializer = TwinSerializer()
        self.simulation_engine = SimulationAdapter()

        self.rollback = RollbackManager(

            self.history

        )

        # ==================================================
        # Core
        # ==================================================

        self.state_manager = StateManager(

            event_bus=self.event_bus

        )

        self.updater = TwinUpdater(

            self.state_manager

        )

        self.synchronizer = Synchronizer(

            manager=self.state_manager,

            validator=self.validator,

            event_bus=self.event_bus

        )

        # ==================================================
        # Register Observers
        # ==================================================

        self.logger = LoggingObserver()

        self.metrics = MetricsObserver()

        self.history_observer = HistoryObserver(

            self.history

        )

        self.version_observer = VersionObserver(

            self.version

        )

        self.validation_observer = ValidationObserver(

            self.validator

        )

        self._register_default_observers()

        # ==================================================
        # Initial Snapshot
        # ==================================================

        self.history.save(

            self.state,

            "Twin Initialized"

        )

    # ======================================================

    @property
    def state(self) -> TwinState:

        return self.state_manager.state

    # ======================================================

    def _register_default_observers(self):
        """
        Register all built-in observers.
        """

        self.event_bus.subscribe_all(

            self.logger

        )

        self.event_bus.subscribe(

            EventType.STATE_UPDATED,

            self.history_observer

        )

        self.event_bus.subscribe(

            EventType.STATE_UPDATED,

            self.version_observer

        )

        self.event_bus.subscribe(

            EventType.STATE_UPDATED,

            self.validation_observer

        )

        self.event_bus.subscribe_all(

            self.metrics

        )

    # ======================================================

    def __repr__(self):

        return (

            f"DigitalTwin("

            f"version={self.state.version})"

        )
            # ======================================================
    # EARTHQUAKE
    # ======================================================

    def load_earthquake(
        self,
        earthquake: Dict[str, Any]
    ):
        """
        Load earthquake information into the Digital Twin.
        """

        self.updater.update_earthquake(
            earthquake
        )

        self.synchronizer.synchronize_earthquake()

        return self.state

    # ======================================================
    # DEM
    # ======================================================

    def load_dem(
        self,
        dem
    ):
        """
        Load Digital Elevation Model.
        """

        self.updater.update_dem(
            dem
        )

        self.synchronizer.synchronize_dem()

        return self.state

    # ======================================================
    # BATHYMETRY
    # ======================================================

    def load_bathymetry(
        self,
        bathymetry
    ):

        self.updater.update_bathymetry(
            bathymetry
        )

        self.synchronizer.synchronize_bathymetry()

        return self.state

    # ======================================================
    # SATELLITE
    # ======================================================

    def load_sentinel1(
        self,
        image
    ):

        self.updater.update_sentinel1(
            image
        )

        self.synchronizer.synchronize()

    # ------------------------------------------------------

    def load_sentinel2(
        self,
        image
    ):

        self.updater.update_sentinel2(
            image
        )

        self.synchronizer.synchronize()

    # ======================================================
    # GENERIC UPDATE
    # ======================================================

    def update(
        self,
        **kwargs
    ):
        """
        Generic update interface.

        Example
        -------
        twin.update(
            earthquake=data,
            dem=dem
        )
        """

        self.updater.update(
            **kwargs
        )

        self.synchronizer.synchronize()

    # ======================================================
    # METADATA
    # ======================================================

    def update_metadata(
        self,
        **kwargs
    ):

        self.updater.update_metadata(
            **kwargs
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate(self):
        """
        Validate current Digital Twin state.
        """

        valid = self.validator.validate_state(
            self.state
        )

        report = self.validator.validation_report()

        return valid, report

    # ======================================================
    # HISTORY
    # ======================================================

    def create_snapshot(
        self,
        message="Manual Snapshot"
    ):

        snapshot = self.history.save(

            self.state,

            message

        )

        return snapshot

    # ------------------------------------------------------

    def history_timeline(self):

        return self.history.timeline()

    # ------------------------------------------------------

    def compare_versions(
        self,
        old_version,
        new_version
    ):

        return self.history.compare(

            old_version,

            new_version

        )
            # ======================================================
    # ROLLBACK
    # ======================================================

    def rollback_to(
        self,
        version: int
    ):
        """
        Restore the Digital Twin to a previous version.
        """

        restored_state = self.rollback.rollback(version)

        self.state_manager.replace_state(
            restored_state
        )

        self.synchronizer.synchronize()

        return self.state

    # ------------------------------------------------------

    def rollback_latest(self):

        restored = self.rollback.latest()

        self.state_manager.replace_state(
            restored
        )

        self.synchronizer.synchronize()

        return self.state

    # ======================================================
    # SERIALIZATION
    # ======================================================

    def save_json(
        self,
        file_path
    ):

        return self.serializer.save_json(

            self.state,

            file_path

        )

    # ------------------------------------------------------

    def save_pickle(
        self,
        file_path
    ):

        return self.serializer.save_pickle(

            self.state,

            file_path

        )

    # ------------------------------------------------------

    def load_pickle(
        self,
        file_path
    ):

        state = self.serializer.load_pickle(

            file_path

        )

        self.state_manager.replace_state(
            state
        )

        self.synchronizer.synchronize()

        return state

    # ------------------------------------------------------

    def checkpoint(
        self,
        directory="checkpoints"
    ):

        return self.serializer.checkpoint(

            self.state,

            directory

        )

    # ======================================================
    # EXPORT
    # ======================================================

    def export_summary(self):

        return self.serializer.export_summary(

            self.state

        )

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.updater.reset()

        self.synchronizer.reset()

        self.history.clear()

        self.version.clear()

        self.history.save(

            self.state,

            "Twin Reset"

        )

        return self.state

    # ======================================================
    # STATUS
    # ======================================================

    def is_ready(self):

        return self.state.is_ready

    # ------------------------------------------------------

    def is_valid(self):

        valid, _ = self.validate()

        return valid

    # ------------------------------------------------------

    def current_version(self):

        return self.state.version

    # ------------------------------------------------------

    def total_versions(self):

        return self.version.total_versions

    # ------------------------------------------------------

    def last_checkpoint(self):

        return self.serializer.last_saved

    # ======================================================
    # INFORMATION
    # ======================================================

    def summary(self):

        return {

            "project":

                self.state.project,

            "scenario":

                self.state.scenario,

            "version":

                self.state.version,

            "ready":

                self.state.is_ready,

            "history":

                len(self.history),

            "events":

                self.event_bus.total_events,

            "syncs":

                self.synchronizer.sync_counter,

            "valid":

                self.is_valid()

        }

    # ------------------------------------------------------

    def print_summary(self):

        print()

        print("=" * 50)

        print(" DIGITAL TWIN SUMMARY ")

        print("=" * 50)

        info = self.summary()

        for key, value in info.items():

            print(f"{key:15}: {value}")

        print("=" * 50)

        print()

    # ======================================================
    # EVENT BUS
    # ======================================================

    def statistics(self):

        return self.event_bus.statistics()

    # ------------------------------------------------------

    def observers(self):

        self.event_bus.print_subscribers()
            # ======================================================
    # SIMULATION ENGINE
    # ======================================================

    def attach_simulation_engine(
        self,
        engine
    ):
        """
        Attach a tsunami simulation engine.

        The engine must implement:

            run(state)

        and return a dictionary containing simulation outputs.
        """

        self.simulation_engine = engine

    # ------------------------------------------------------

    def detach_simulation_engine(self):

        self.simulation_engine = None

    # ------------------------------------------------------

    def has_simulation_engine(self):

        return hasattr(self, "simulation_engine") \
            and self.simulation_engine is not None

    # ======================================================
    # RUN SIMULATION
    # ======================================================

    def run_simulation(self):
        """
        Execute tsunami simulation.
        """

        if not self.has_simulation_engine():

            raise RuntimeError(

                "No simulation engine attached."

            )

        if not self.state.is_ready:

            raise RuntimeError(

                "Twin is not ready."

            )

        results = self.simulation_engine.run(

            self.state

        )

        self.updater.update_simulation(

            tsunami=results.get("tsunami"),

            inundation=results.get("inundation"),

            hazard_map=results.get("hazard_map"),

            evacuation_map=results.get(

                "evacuation_map"

            )

        )

        self.synchronizer.synchronize_simulation()

        self.create_snapshot(

            "Simulation Completed"

        )

        return results
        # ======================================================
    # PROJECT SAVE
    # ======================================================

    def save_project(
        self,
        directory="project"
    ):

        directory = Path(directory)

        directory.mkdir(

            parents=True,

            exist_ok=True

        )

        self.save_pickle(

            directory / "digital_twin.pkl"

        )

        self.save_json(

            directory / "digital_twin.json"

        )

        return directory

    # ------------------------------------------------------

    def load_project(
        self,
        file
    ):

        return self.load_pickle(file)
        # ======================================================
    # HEALTH
    # ======================================================

    def health(self):

        valid, report = self.validate()

        return {

            "ready":

                self.state.is_ready,

            "valid":

                valid,

            "version":

                self.state.version,

            "history":

                len(self.history),

            "events":

                self.event_bus.total_events,

            "syncs":

                self.synchronizer.sync_counter,

            "errors":

                report["error_count"],

            "warnings":

                report["warning_count"]

        }
            # ======================================================
    # DEMO
    # ======================================================

    def info(self):

        print()

        print("=" * 60)

        print(" DIGITAL TWIN ")

        print("=" * 60)

        print(

            "Project :",

            self.state.project

        )

        print(

            "Scenario:",

            self.state.scenario

        )

        print(

            "Version :",

            self.state.version

        )

        print(

            "Ready   :",

            self.state.is_ready

        )

        print(

            "Events  :",

            self.event_bus.total_events

        )

        print(

            "History :",

            len(self.history)

        )

        print(

            "Syncs   :",

            self.synchronizer.sync_counter

        )

        print("=" * 60)

        print()
            # ======================================================
    # SIMULATION STATUS
    # ======================================================

    def simulation_ready(self):

        state = self.state

        return (

            state.earthquake is not None

            and

            state.dem is not None

            and

            state.bathymetry is not None

        )

    # ------------------------------------------------------

    def __str__(self):

        return (

            f"DigitalTwin("

            f"version={self.state.version}, "

            f"ready={self.state.is_ready})"

        )
        