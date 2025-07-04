from event_horizon.aggregates import Aggregate
from event_horizon.events import Event, deserialize_event


class EventStore:
    def __init__(self):
        self.events = []

    def save(self, aggregate: Aggregate):
        events = aggregate.get_uncommitted_events()
        for event in events:
            event_dict = event.to_dict()
            self.events.append(event_dict)
        aggregate.clear_uncommitted_events()

    def load(self, aggregate_type: type[Aggregate], event_type: type[Event], aggregate_id: str):
        events = []
        for event_json in self.events:
            event = deserialize_event(event_json)
            if event.aggregate_id == aggregate_id and isinstance(event, event_type):
                events.append(event)
        return aggregate_type.rehydrate(aggregate_id, events)
