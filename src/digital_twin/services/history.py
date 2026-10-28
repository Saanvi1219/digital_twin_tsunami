from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from src.digital_twin.models.snapshot import Snapshot
from src.digital_twin.models.dt_state import TwinState


class HistoryManager:
    """
    Stores every state transition of the Digital Twin.

    Example
    -------

    history.save(state)

    history.latest()

    history.rollback(5)

    history.compare(3,5)

    """

    def __init__(self):

        self._history: List[Snapshot] = []

    # --------------------------------------------------

    @property
    def total_versions(self):

        return len(self._history)

    # --------------------------------------------------

    def is_empty(self):

        return len(self._history) == 0

    # --------------------------------------------------

    def save(
        self,
        state: TwinState,
        message: str = "Automatic Snapshot"
    ):

        snapshot = Snapshot.from_state(

            twin_state=state,

            message=message

        )

        self._history.append(snapshot)

        return snapshot

    # --------------------------------------------------

    def latest(self) -> Optional[Snapshot]:

        if self.is_empty():

            return None

        return self._history[-1]

    # --------------------------------------------------

    def first(self):

        if self.is_empty():

            return None

        return self._history[0]

    # --------------------------------------------------

    def get(
        self,
        version: int
    ) -> Snapshot:

        for snapshot in self._history:

            if snapshot.version == version:

                return snapshot

        raise ValueError(

            f"Version {version} does not exist."

        )

    # --------------------------------------------------

    def rollback(
        self,
        version: int
    ) -> Snapshot:

        return self.get(version)

    # --------------------------------------------------

    def delete_after(
        self,
        version: int
    ):

        self._history = [

            s

            for s in self._history

            if s.version <= version

        ]

    # --------------------------------------------------

    def compare(
        self,
        old_version: int,
        new_version: int
    ):

        old = self.get(old_version)

        new = self.get(new_version)

        differences = {}

        keys = set(old.state.keys()) | set(new.state.keys())

        for key in keys:

            old_value = old.state.get(key)

            new_value = new.state.get(key)

            if old_value != new_value:

                differences[key] = {

                    "old": old_value,

                    "new": new_value

                }

        return differences

    # --------------------------------------------------

    def versions(self):

        return [

            snapshot.version

            for snapshot in self._history

        ]

    # --------------------------------------------------

    def timeline(self):

        timeline = []

        for snapshot in self._history:

            timeline.append({

                "version": snapshot.version,

                "timestamp":

                    snapshot.timestamp.isoformat(),

                "message": snapshot.message

            })

        return timeline

    # --------------------------------------------------

    def export_json(
        self,
        path: str
    ):

        path = Path(path)

        data = []

        for snapshot in self._history:

            data.append({

                "version": snapshot.version,

                "timestamp":

                    snapshot.timestamp.isoformat(),

                "message": snapshot.message,

                "state": snapshot.state

            })

        with open(

            path,

            "w",

            encoding="utf8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4

            )

    # --------------------------------------------------

    def clear(self):

        self._history.clear()

    # --------------------------------------------------

    def __len__(self):

        return len(self._history)

    # --------------------------------------------------

    def __getitem__(

        self,

        item

    ):

        return self._history[item]

    # --------------------------------------------------

    def __iter__(self):

        return iter(self._history)

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"HistoryManager("

            f"versions={len(self._history)})"

        )