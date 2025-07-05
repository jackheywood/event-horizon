from datetime import datetime

from event_horizon.events import LightCreated, LightSwitchedOn, LightSwitchedOff, Event
from .base_aggregate import Aggregate


class LightAggregate(Aggregate):
    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.is_on = False

    @classmethod
    def create(cls, aggregate_id: str, is_on: bool = False):
        aggregate = cls(aggregate_id)
        aggregate.raise_event(LightCreated(datetime.now(), aggregate_id, is_on))
        return aggregate

    @classmethod
    def rehydrate(cls, aggregate_id: str, events: list[Event]):
        aggregate = cls(aggregate_id)
        aggregate.apply_events(events)
        return aggregate

    def turn_on(self):
        self.raise_event(LightSwitchedOn(datetime.now(), self.aggregate_id))

    def turn_off(self):
        self.raise_event(LightSwitchedOff(datetime.now(), self.aggregate_id))

    def apply(self, event):
        if isinstance(event, LightCreated):
            if self._was_created:
                raise Exception("Light already created")
            self.is_on = event.is_on
            self._created = True

        elif isinstance(event, LightSwitchedOn):
            if self.is_on:
                raise Exception("Light is already switched on")
            self.is_on = True

        elif isinstance(event, LightSwitchedOff):
            if not self.is_on:
                raise Exception("Light is already switched off")
            self.is_on = False

        else:
            raise Exception(f"Unknown event {event.__class__.__name__}")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.aggregate_id} is_on={self.is_on}>"
