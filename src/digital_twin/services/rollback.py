"""
rollback.py

Rollback engine for the Digital Twin.

Responsible for restoring previous states safely using HistoryManager.
"""

from __future__ import annotations

from typing import Optional

from src.digital_twin.models.snapshot import Snapshot
from src.digital_twin.models.dt_state import TwinState

from src.digital_twin.services.history import HistoryManager

from src.digital_twin.exceptions import StateError


class RollbackManager:
    """
    Restores previous Digital Twin states from history.
    """

    def __init__(self, history: HistoryManager):

        self.history = history

        self.current_version: Optional[int] = None
            # --------------------------------------------------

    def restore_snapshot(
        self,
        snapshot: Snapshot
    ) -> TwinState:
        """
        Restore a TwinState from a Snapshot.
        """

        data = snapshot.state

        state = TwinState()

        for key, value in data.items():

            if hasattr(state, key):

                setattr(state, key, value)

        self.current_version = snapshot.version

        return state
        # --------------------------------------------------

    def rollback(
        self,
        version: int
    ) -> TwinState:
        """
        Restore the Digital Twin to a previous version.
        """

        snapshot = self.history.get(version)

        return self.restore_snapshot(snapshot)
        # --------------------------------------------------

    def latest(self) -> TwinState:
        """
        Restore the latest available snapshot.
        """

        snapshot = self.history.latest()

        if snapshot is None:

            raise StateError(

                "History is empty."

            )

        return self.restore_snapshot(snapshot)
        # --------------------------------------------------

    def first(self) -> TwinState:

        snapshot = self.history.first()

        if snapshot is None:

            raise StateError(

                "History is empty."

            )

        return self.restore_snapshot(snapshot)
        # --------------------------------------------------

    def first(self) -> TwinState:

        snapshot = self.history.first()

        if snapshot is None:

            raise StateError(

                "History is empty."

            )

        return self.restore_snapshot(snapshot)
        # --------------------------------------------------

    def previous(self) -> TwinState:

        if self.current_version is None:

            raise StateError(

                "No active version."

            )

        version = self.current_version - 1

        return self.rollback(version)

    # --------------------------------------------------

    def next(self) -> TwinState:

        if self.current_version is None:

            raise StateError(

                "No active version."

            )

        version = self.current_version + 1

        return self.rollback(version)
        # --------------------------------------------------

    def available_versions(self):

        return self.history.versions()

    # --------------------------------------------------

    def timeline(self):

        return self.history.timeline()
        # --------------------------------------------------

    def compare(
        self,
        version_a: int,
        version_b: int
    ):

        return self.history.compare(

            version_a,

            version_b

        )
            # --------------------------------------------------

    def reset(self):

        self.current_version = None

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"RollbackManager("

            f"current_version={self.current_version})"

        )