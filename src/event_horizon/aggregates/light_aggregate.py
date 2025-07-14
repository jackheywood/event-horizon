from event_horizon.events import LightCreated, LightSwitchedOn, LightSwitchedOff
from .binary_device_aggregate import BinaryDeviceAggregate


class LightAggregate(BinaryDeviceAggregate):
    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id, "is_on")

    @property
    def _created_event(self):
        return LightCreated

    @property
    def _on_state_event(self):
        return LightSwitchedOn

    @property
    def _off_state_event(self):
        return LightSwitchedOff

    @property
    def _on_state_name(self):
        return "switched on"

    @property
    def _off_state_name(self):
        return "switched off"

    @classmethod
    def create(cls, aggregate_id: str, is_on: bool = False):
        return cls._create_internal(LightCreated, aggregate_id, is_on=is_on)

    def turn_on(self):
        self._change_state(LightSwitchedOn)

    def turn_off(self):
        self._change_state(LightSwitchedOff)
