from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Optional

from src.digital_twin.models.dt_state import TwinState
from src.digital_twin.models.snapshot import Snapshot

from src.digital_twin.events.event import (
    create_state_update_event,
)

from src.digital_twin.events.event_bus import EventBus


class StateManager:
    """
    Owns the current TwinState.

    No other component should modify TwinState directly.
    """

    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
    ):

        self._state = TwinState()

        self._event_bus = event_bus

    # --------------------------------------------------

    @property
    def state(self) -> TwinState:

        return self._state
        # --------------------------------------------------

    def replace_state(
        self,
        state: TwinState
    ):

        self._state = state

        self.publish()

    # --------------------------------------------------

    def clone(self):

        return deepcopy(self._state)

    # --------------------------------------------------

    def snapshot(
        self,
        message: str = "Snapshot"
    ) -> Snapshot:

        return Snapshot.from_state(

            self._state,

            message

        )
            # --------------------------------------------------

    def publish(self):

        if self._event_bus is None:

            return

        event = create_state_update_event(

            source="StateManager",

            payload={

                "state": self._state

            }

        )

        self._event_bus.publish(event)
            # --------------------------------------------------

    def update(
        self,
        **kwargs
    ):

        """
        Generic update.

        Example
        -------

        update(
            earthquake=data,
            dem=dem
        )
        """

        modified = False

        for key, value in kwargs.items():

            if hasattr(self._state, key):

                setattr(

                    self._state,

                    key,

                    value

                )

                modified = True

        if modified:

            self.touch()

            self.publish()
                # --------------------------------------------------

    def touch(self):

        """
        Updates timestamp and version.
        """

        self._state.increment_version()

        self._state.timestamp = datetime.utcnow()
            # --------------------------------------------------

    def clear_predictions(self):

        self._state.clear_predictions()

        self.publish()

    # --------------------------------------------------

    def reset_simulation(self):

        self._state.reset_simulation()

        self.publish()

    # --------------------------------------------------

    def reset(self):

        self._state = TwinState()

        self.publish()
            # --------------------------------------------------

    def set_metadata(
        self,
        key,
        value
    ):

        self._state.metadata[key] = value

        self.publish()

    # --------------------------------------------------

    def metadata(
        self):

        return self._state.metadata
        # --------------------------------------------------

    def summary(self):

        return {

            "version":

                self._state.version,

            "timestamp":

                self._state.timestamp,

            "ready":

                self._state.is_ready,

            "project":

                self._state.project,

            "scenario":

                self._state.scenario

        }
            # --------------------------------------------------

    def to_dict(self):

        return self._state.to_dict()

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"StateManager("

            f"version={self._state.version})"

        )