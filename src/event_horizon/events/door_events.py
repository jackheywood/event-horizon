from dataclasses import dataclass

from .base_event import Event


@dataclass(frozen=True)
class DoorEvent(Event):
    @classmethod
    def category(cls) -> str:
        return DoorEvent.__name__


@dataclass(frozen=True)
class DoorCreated(DoorEvent):
    is_open: bool

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["is_open"] = self.is_open
        return data


@dataclass(frozen=True)
class DoorOpened(DoorEvent):
    pass


@dataclass(frozen=True)
class DoorClosed(DoorEvent):
    pass
