from event_horizon.aggregates import DoorAggregate
from event_horizon.commands import Command, NewDoor, OpenDoor, CloseDoor
from event_horizon.domain import EventStore
from event_horizon.events import DoorEvent


class DoorHandler:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def handle(self, command: Command):
        if isinstance(command, NewDoor):
            if self.event_store.exists(DoorEvent, command.aggregate_id):
                raise Exception(f"Door with id '{command.aggregate_id}' already exists")
            aggregate = DoorAggregate.create(command.aggregate_id, command.is_open)
            self.event_store.save(aggregate)

        elif isinstance(command, OpenDoor):
            aggregate = self._load_aggregate(command.aggregate_id)
            aggregate.open()
            self.event_store.save(aggregate)

        elif isinstance(command, CloseDoor):
            aggregate = self._load_aggregate(command.aggregate_id)
            aggregate.close()
            self.event_store.save(aggregate)

        else:
            raise Exception(f"Unknown command {command.__class__.__name__}")

    def _load_aggregate(self, aggregate_id: str):
        return self.event_store.load(DoorAggregate, DoorEvent, aggregate_id)
