from event_horizon.aggregates import Aggregate
from event_horizon.event_repository import EventRepository
from event_horizon.events import deserialize_event, Event


class EventStore:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def save(self, aggregate: Aggregate):
        events = aggregate.get_uncommitted_events()
        for event in events:
            self.event_repository.save(event.to_dict())
        aggregate.clear_uncommitted_events()

    def load(self, aggregate_type: type[Aggregate], event_type: type[Event], aggregate_id: str):
        events = []
        for event_dict in self.event_repository.load(event_type.category(), aggregate_id):
            event = deserialize_event(event_dict)
            events.append(event)
        return aggregate_type.rehydrate(aggregate_id, events)
