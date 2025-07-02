from abc import ABC, abstractmethod

from event_horizon.events import Event


class Aggregate(ABC):
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self._changes = []
        self._created = False

    def raise_event(self, event: Event):
        self._changes.append(event)
        self.apply(event)

    def get_changes(self):
        return self._changes.copy()

    def clear_changes(self):
        self._changes.clear()

    def replay_events(self, events: list[Event]):
        for event in events:
            self.apply(event)

    @abstractmethod
    def apply(self, event: Event):
        pass
