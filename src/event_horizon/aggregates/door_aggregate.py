from datetime import datetime

from event_horizon.events import DoorCreated, DoorOpened, DoorClosed, Event
from .base_aggregate import Aggregate


class DoorAggregate(Aggregate):
    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.is_open = False

    @classmethod
    def create(cls, aggregate_id: str, is_open: bool = False):
        aggregate = cls(aggregate_id)
        aggregate._raise_event(DoorCreated(datetime.now(), aggregate_id, is_open))
        return aggregate

    @classmethod
    def rehydrate(cls, aggregate_id: str, events: list[Event]):
        aggregate = cls(aggregate_id)
        aggregate._apply_events(events)
        return aggregate

    def open(self):
        self._raise_event(DoorOpened(datetime.now(), self.aggregate_id))

    def close(self):
        self._raise_event(DoorClosed(datetime.now(), self.aggregate_id))

    def _apply(self, event):
        if isinstance(event, DoorCreated):
            if self._was_created:
                raise Exception("Door has already been created")
            self.is_open = event.is_open
            self._was_created = True

        elif isinstance(event, DoorOpened):
            if self.is_open:
                raise Exception("Door is already open")
            self.is_open = True

        elif isinstance(event, DoorClosed):
            if not self.is_open:
                raise Exception("Door is already closed")
            self.is_open = False

        else:
            raise Exception(f"Unknown event {event.__class__.__name__}")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.aggregate_id} is_open={self.is_open}>"
