from abc import ABC, abstractmethod

from event_horizon.events import Event


class Aggregate(ABC):
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self._changes = []
        self._was_created = False

    def get_uncommitted_events(self):
        return self._changes.copy()

    def clear_uncommitted_events(self):
        self._changes.clear()

    def _raise_event(self, event: Event):
        self._changes.append(event)
        self._apply(event)

    def _apply_events(self, events: list[Event]):
        for event in events:
            self._apply(event)

    @classmethod
    @abstractmethod
    def create(cls, aggregate_id: str, **kwargs):
        """Creates a new aggregate and raises a creation event"""
        ...

    @classmethod
    @abstractmethod
    def rehydrate(cls, aggregate_id: str, events: list[Event]):
        """Creates a new aggregate from a list of events"""
        ...

    @abstractmethod
    def _apply(self, event: Event):
        """Appies an event to the aggregate"""
        ...
