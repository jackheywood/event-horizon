from abc import ABC, abstractmethod
from datetime import datetime

from .base_aggregate import Aggregate


class BinaryDeviceAggregate(Aggregate, ABC):
    def __init__(self, aggregate_id: str, state_attr: str):
        super().__init__(aggregate_id)
        self._state_attr = state_attr
        setattr(self, state_attr, False)

    @property
    @abstractmethod
    def _on_state_event(self) -> type:
        """The event class that represents switching on"""
        ...

    @property
    @abstractmethod
    def _off_state_event(self) -> type:
        """The event class that represents switching off"""
        ...

    @property
    @abstractmethod
    def _on_state_name(self):
        """The name of the on state"""

    @property
    @abstractmethod
    def _off_state_name(self):
        """The name of the off state"""

    def _change_state(self, event_cls):
        self._raise_event(event_cls(datetime.now(), self.aggregate_id))

    def _apply(self, event):
        if isinstance(event, self._created_event):
            if self._was_created:
                raise Exception(f"{self._pretty_name} has already been created")
            setattr(self, self._state_attr, getattr(event, self._state_attr))
            self._was_created = True

        elif isinstance(event, self._on_state_event):
            if getattr(self, self._state_attr) is True:
                raise Exception(f"{self._pretty_name} is already {self._on_state_name}")
            setattr(self, self._state_attr, True)

        elif isinstance(event, self._off_state_event):
            if getattr(self, self._state_attr) is False:
                raise Exception(f"{self._pretty_name} is already {self._off_state_name}")
            setattr(self, self._state_attr, False)

        else:
            raise Exception(f"Unknown event {event.__class__.__name__}")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"{self.aggregate_id} "
            f"{self._state_attr}={getattr(self, self._state_attr)}>"
        )
