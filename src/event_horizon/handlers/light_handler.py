from event_horizon.aggregates import LightAggregate
from event_horizon.commands import Command, NewLight, TurnOnLight, TurnOffLight
from event_horizon.event_store import EventStore
from event_horizon.events import LightEvent


class LightHandler:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def handle(self, command: Command):
        if isinstance(command, NewLight):
            aggregate = LightAggregate.create(command.aggregate_id, command.is_on)
            self.event_store.save(aggregate)

        elif isinstance(command, TurnOnLight):
            aggregate = self.event_store.load(LightAggregate, LightEvent, command.aggregate_id)
            aggregate.turn_on()
            self.event_store.save(aggregate)

        elif isinstance(command, TurnOffLight):
            aggregate = self.event_store.load(LightAggregate, LightEvent, command.aggregate_id)
            aggregate.turn_off()
            self.event_store.save(aggregate)

        else:
            raise Exception(f"Unknown command {command.__class__.__name__}")
