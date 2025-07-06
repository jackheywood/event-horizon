from typing import TypeVar

from event_horizon.aggregates import Aggregate
from event_horizon.events import deserialize_event, Event
from event_horizon.persistence import EventRepository

TAggregate = TypeVar("TAggregate", bound=Aggregate)


class EventStore:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def save(self, aggregate: Aggregate) -> None:
        events = aggregate.get_uncommitted_events()
        for event in events:
            self.event_repo.save(event.to_dict())
        aggregate.clear_uncommitted_events()

    def load_all(
            self,
            aggregate_type: type[TAggregate],
            event_type: type[Event],
    ) -> list[TAggregate]:
        aggregate_events = self.event_repo.load_all(event_type.category())
        return [
            aggregate_type.rehydrate(
                aggregate_id,
                [deserialize_event(e) for e in events],
            )
            for aggregate_id, events in sorted(aggregate_events.items())
        ]

    def load(
            self,
            aggregate_type: type[TAggregate],
            event_type: type[Event],
            aggregate_id: str,
    ) -> TAggregate:
        events = []

        for event_dict in self.event_repo.load(
                event_type.category(),
                aggregate_id,
        ):
            event = deserialize_event(event_dict)
            events.append(event)

        if not events:
            raise ValueError(
                f"No events found for {aggregate_type.__name__} "
                f"with id {aggregate_id}"
            )

        return aggregate_type.rehydrate(aggregate_id, events)

    def exists(self, event_type: type[Event], aggregate_id: str) -> bool:
        return any(self.event_repo.load(event_type.category(), aggregate_id))
