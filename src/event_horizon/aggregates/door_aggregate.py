from event_horizon.events import DoorCreated, DoorOpened, DoorClosed
from .binary_device_aggregate import BinaryDeviceAggregate


class DoorAggregate(BinaryDeviceAggregate):
    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id, "is_open")

    @property
    def _created_event(self):
        return DoorCreated

    @property
    def _on_state_event(self):
        return DoorOpened

    @property
    def _off_state_event(self):
        return DoorClosed

    @property
    def _on_state_name(self):
        return "open"

    @property
    def _off_state_name(self):
        return "closed"

    @classmethod
    def create(cls, aggregate_id: str, is_open: bool = False):
        return cls._create_internal(DoorCreated, aggregate_id, is_open=is_open)

    def open(self):
        self._change_state(DoorOpened)

    def close(self):
        self._change_state(DoorClosed)
