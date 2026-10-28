"""
event_bus.py
============

Central Event Bus for the Digital Twin.

The EventBus provides a publish-subscribe architecture where
components communicate using events instead of direct references.

Benefits
--------
✔ Loose coupling
✔ Extensible
✔ Modular
✔ Easy testing
✔ Scalable

Author
------
Digital Twin Engine
"""

from __future__ import annotations

import logging

from collections import defaultdict

from typing import Dict, List

from .event import Event, EventType
from .observer import Observer

logger = logging.getLogger(__name__)


class EventBus:
    """
    Central event dispatcher.

    All events inside the Digital Twin flow through this class.
    """

    def __init__(self):

        # Event-specific subscribers
        self._subscribers: Dict[
            EventType,
            List[Observer]
        ] = defaultdict(list)

        # Global subscribers
        self._global_subscribers: List[Observer] = []

        # Event history
        self._history: List[Event] = []

        # Statistics
        self._published_events = 0

    # =======================================================
    # SUBSCRIBE
    # =======================================================

    def subscribe(
        self,
        event_type: EventType,
        observer: Observer
    ):

        if observer not in self._subscribers[event_type]:

            self._subscribers[event_type].append(
                observer
            )

            logger.info(

                "Observer %s subscribed to %s",

                observer.name,

                event_type.value

            )

    # =======================================================

    def subscribe_all(
        self,
        observer: Observer
    ):

        if observer not in self._global_subscribers:

            self._global_subscribers.append(
                observer
            )

    # =======================================================

    def unsubscribe(
        self,
        event_type: EventType,
        observer: Observer
    ):

        if observer in self._subscribers[event_type]:

            self._subscribers[event_type].remove(
                observer
            )

    # =======================================================

    def unsubscribe_all(
        self,
        observer: Observer
    ):

        if observer in self._global_subscribers:

            self._global_subscribers.remove(
                observer
            )

    # =======================================================
    # PUBLISH
    # =======================================================

    def publish(
        self,
        event: Event
    ):

        """
        Publish an event.

        Every subscribed observer receives the event.
        """

        self._published_events += 1

        self._history.append(event)

        # Notify event-specific observers

        for observer in self._subscribers[
            event.event_type
        ]:

            observer.update(event)

        # Notify global observers

        for observer in self._global_subscribers:

            observer.update(event)

        event.mark_handled()

    # =======================================================
    # HISTORY
    # =======================================================

    @property
    def history(self):

        return self._history

    # =======================================================

    def latest_event(self):

        if not self._history:

            return None

        return self._history[-1]

    # =======================================================

    def events_of_type(
        self,
        event_type: EventType
    ):

        return [

            event

            for event in self._history

            if event.event_type == event_type

        ]

    # =======================================================

    def clear_history(self):

        self._history.clear()

    # =======================================================
    # STATISTICS
    # =======================================================

    @property
    def total_events(self):

        return self._published_events

    # =======================================================

    def total_subscribers(self):

        total = len(self._global_subscribers)

        for observers in self._subscribers.values():

            total += len(observers)

        return total

    # =======================================================

    def statistics(self):

        return {

            "events_published":

                self._published_events,

            "history_size":

                len(self._history),

            "subscribers":

                self.total_subscribers()

        }

    # =======================================================
    # DEBUGGING
    # =======================================================

    def print_subscribers(self):

        print("\n===== EVENT BUS =====")

        for event_type, observers in self._subscribers.items():

            print(

                f"\n{event_type.value}"

            )

            for observer in observers:

                print(

                    "   ->",

                    observer.name

                )

        print("\nGlobal Subscribers")

        for observer in self._global_subscribers:

            print(

                "   ->",

                observer.name

            )

    # =======================================================

    def reset(self):

        self._subscribers.clear()

        self._global_subscribers.clear()

        self._history.clear()

        self._published_events = 0

    # =======================================================

    def __len__(self):

        return len(self._history)

    # =======================================================

    def __repr__(self):

        return (

            f"EventBus("

            f"events={len(self._history)}, "

            f"subscribers={self.total_subscribers()})"

        )