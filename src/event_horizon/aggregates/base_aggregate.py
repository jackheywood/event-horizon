from abc import ABC, abstractmethod
from datetime import datetime

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
    def rehydrate(cls, aggregate_id: str, events: list[Event]):
        """Creates a new aggregate from a list of events"""
        aggregate = cls(aggregate_id)
        aggregate._apply_events(events)
        return aggregate

    @classmethod
    def _create_internal(cls, created_event_cls, aggregate_id: str, **kwargs):
        """Creates a new aggregate and raises a creation event"""
        aggregate = cls(aggregate_id)
        aggregate._raise_event(created_event_cls(datetime.now(), aggregate_id, **kwargs))
        return aggregate

    @abstractmethod
    def _apply(self, event: Event):
        """Appies an event to the aggregate"""
        ...

    @property
    @abstractmethod
    def _created_event(self) -> type:
        """The event class that represents creation"""
        ...

    @property
    def _pretty_name(self) -> str:
        return self.__class__.__name__.replace("Aggregate", "")
