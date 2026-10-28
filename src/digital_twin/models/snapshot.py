"""
snapshot.py

Immutable snapshot of a Digital Twin state.

Every time the Digital Twin changes, a Snapshot is created and
stored in HistoryManager. Snapshots are never modified after
creation, enabling rollback and reproducibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from copy import deepcopy
from typing import Any, Dict

from .dt_state import TwinState


@dataclass(frozen=True, slots=True)
class Snapshot:
    """
    Immutable copy of a TwinState.
    """

    version: int
    timestamp: datetime

    state: Dict[str, Any] = field(default_factory=dict)

    message: str = "State Snapshot"

    # ------------------------------------------

    @classmethod
    def from_state(
        cls,
        twin_state: TwinState,
        message: str = "Automatic Snapshot"
    ) -> "Snapshot":
        """
        Create a Snapshot from a TwinState.
        """

        return cls(
            version=twin_state.version,
            timestamp=twin_state.timestamp,
            state=deepcopy(twin_state.to_dict()),
            message=message,
        )

    # ------------------------------------------

    def get(self, key: str, default=None):
        """
        Retrieve a value from the snapshot.
        """

        return self.state.get(key, default)

    # ------------------------------------------

    def has(self, key: str) -> bool:
        """
        Check if a field exists.
        """

        return key in self.state

    # ------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Lightweight summary.
        """

        return {

            "version": self.version,

            "timestamp": self.timestamp.isoformat(),

            "message": self.message,

            "fields": list(self.state.keys())

        }

    # ------------------------------------------

    def __len__(self):

        return len(self.state)

    # ------------------------------------------

    def __contains__(self, item):

        return item in self.state

    # ------------------------------------------

    def __getitem__(self, item):

        return self.state[item]

    # ------------------------------------------

    def __repr__(self):

        return (

            f"Snapshot("
            f"version={self.version}, "
            f"time={self.timestamp}, "
            f"fields={len(self.state)})"

        )